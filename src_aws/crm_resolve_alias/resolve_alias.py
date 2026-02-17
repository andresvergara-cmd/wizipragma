"""
CRM - Resolve Alias Lambda
Resolves beneficiary alias to account with fuzzy matching
Example: "mi hermano" -> Juan López (account: acc-789)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import (
    StructuredLogger,
    extract_correlation_id,
    DynamoDBHelper,
    EventBridgeHelper,
    validate_event,
    CentliError,
    AliasNotFoundError
)


BENEFICIARIES_TABLE = os.environ.get('BENEFICIARIES_TABLE', 'centli-beneficiaries')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')


def lambda_handler(event, context):
    """Lambda handler for alias resolution"""
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('crm-resolve-alias', correlation_id)
    
    try:
        logger.info('Processing alias resolution')
        
        detail = validate_event(event, ['user_id', 'alias'])
        user_id = detail['user_id']
        alias = detail['alias']
        
        logger.info('Resolving alias', alias=alias)
        
        # Normalize alias for matching
        alias_normalized = normalize_alias(alias)
        
        # Query beneficiaries by alias (GSI)
        db_helper = DynamoDBHelper(BENEFICIARIES_TABLE)
        beneficiaries = db_helper.query(
            key_condition_expression='alias_lower = :alias AND user_id = :user_id',
            expression_values={
                ':alias': alias_normalized,
                ':user_id': user_id
            },
            index_name='alias-index'
        )
        
        if beneficiaries:
            # Exact match found
            beneficiary = beneficiaries[0]
            logger.info('Exact alias match found', beneficiary_id=beneficiary.get('beneficiary_id'))
        else:
            # Try fuzzy matching
            logger.info('No exact match, trying fuzzy matching')
            beneficiary = fuzzy_match_alias(db_helper, user_id, alias_normalized, logger)
            
            if not beneficiary:
                raise AliasNotFoundError(alias)
        
        # Prepare response
        response_data = {
            'alias': alias,
            'beneficiary_id': beneficiary.get('beneficiary_id'),
            'name': beneficiary.get('name'),
            'account_id': beneficiary.get('account_id'),
            'relationship': beneficiary.get('relationship')
        }
        
        # Publish success event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_success_event(
            event_type='ALIAS_RESOLUTION_RESPONSE',
            data=response_data,
            correlation_id=correlation_id,
            source='crm',
            user_id=user_id
        )
        
        logger.info('Alias resolved successfully', beneficiary_name=beneficiary.get('name'))
        
        return {
            'statusCode': 200,
            'body': {
                'message': 'Alias resolved',
                'beneficiary_id': beneficiary.get('beneficiary_id'),
                'correlation_id': correlation_id
            }
        }
        
    except CentliError as e:
        logger.error('Business error', error_code=e.error_code, error_message=e.message)
        
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='ALIAS_RESOLUTION_FAILED',
            error_message=e.message,
            error_code=e.error_code,
            correlation_id=correlation_id,
            source='crm',
            user_id=detail.get('user_id') if 'detail' in locals() else None
        )
        
        return {
            'statusCode': 400,
            'body': {
                'error': e.error_code,
                'message': e.message,
                'correlation_id': correlation_id
            }
        }
        
    except Exception as e:
        logger.error('Unexpected error', error=str(e))
        
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='ALIAS_RESOLUTION_FAILED',
            error_message='Internal server error',
            error_code='INTERNAL_ERROR',
            correlation_id=correlation_id,
            source='crm'
        )
        
        return {
            'statusCode': 500,
            'body': {
                'error': 'INTERNAL_ERROR',
                'message': 'Internal server error',
                'correlation_id': correlation_id
            }
        }


def normalize_alias(alias: str) -> str:
    """
    Normalize alias for matching
    - Lowercase
    - Trim whitespace
    - Remove accents (basic)
    """
    normalized = alias.lower().strip()
    
    # Basic accent removal (Spanish)
    accent_map = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ñ': 'n', 'ü': 'u'
    }
    
    for accented, plain in accent_map.items():
        normalized = normalized.replace(accented, plain)
    
    return normalized


def fuzzy_match_alias(db_helper, user_id, alias_normalized, logger):
    """
    Fuzzy match alias against all user beneficiaries
    Uses simple substring matching
    """
    # Get all beneficiaries for user
    beneficiaries = db_helper.query(
        key_condition_expression='user_id = :user_id',
        expression_values={':user_id': user_id}
    )
    
    logger.info('Fuzzy matching against beneficiaries', count=len(beneficiaries))
    
    # Try substring matching
    for beneficiary in beneficiaries:
        beneficiary_alias = normalize_alias(beneficiary.get('alias', ''))
        beneficiary_name = normalize_alias(beneficiary.get('name', ''))
        
        # Check if alias is substring of beneficiary alias or name
        if alias_normalized in beneficiary_alias or alias_normalized in beneficiary_name:
            logger.info('Fuzzy match found', 
                       beneficiary_id=beneficiary.get('beneficiary_id'),
                       matched_field='alias' if alias_normalized in beneficiary_alias else 'name')
            return beneficiary
        
        # Check if beneficiary alias is substring of input alias
        if beneficiary_alias in alias_normalized:
            logger.info('Fuzzy match found (reverse)', 
                       beneficiary_id=beneficiary.get('beneficiary_id'))
            return beneficiary
    
    # No match found
    return None
