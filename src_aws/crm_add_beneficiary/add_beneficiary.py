"""
CRM - Add Beneficiary Lambda
Adds a new beneficiary for a user
"""

import os
import sys
import uuid
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import (
    StructuredLogger,
    extract_correlation_id,
    DynamoDBHelper,
    EventBridgeHelper,
    validate_event,
    validate_required_fields,
    CentliError
)


BENEFICIARIES_TABLE = os.environ.get('BENEFICIARIES_TABLE', 'centli-beneficiaries')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')


def lambda_handler(event, context):
    """Lambda handler for add beneficiary"""
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('crm-add-beneficiary', correlation_id)
    
    try:
        logger.info('Processing add beneficiary request')
        
        detail = validate_event(event, ['user_id', 'name', 'alias', 'account_id'])
        user_id = detail['user_id']
        name = detail['name']
        alias = detail['alias']
        account_id = detail['account_id']
        relationship = detail.get('relationship', 'other')
        
        logger.info('Adding beneficiary', name=name, alias=alias)
        
        # Normalize alias
        alias_lower = alias.lower().strip()
        
        # Check if alias already exists for this user
        db_helper = DynamoDBHelper(BENEFICIARIES_TABLE)
        existing = db_helper.query(
            key_condition_expression='alias_lower = :alias AND user_id = :user_id',
            expression_values={
                ':alias': alias_lower,
                ':user_id': user_id
            },
            index_name='alias-index'
        )
        
        if existing:
            raise CentliError(
                f'Alias already exists: {alias}',
                'ALIAS_ALREADY_EXISTS'
            )
        
        # Create beneficiary
        beneficiary_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        beneficiary = {
            'user_id': user_id,
            'beneficiary_id': beneficiary_id,
            'name': name,
            'alias': alias,
            'alias_lower': alias_lower,
            'account_id': account_id,
            'relationship': relationship,
            'created_at': timestamp
        }
        
        db_helper.put_item(beneficiary)
        
        logger.info('Beneficiary added', beneficiary_id=beneficiary_id)
        
        response_data = {
            'beneficiary_id': beneficiary_id,
            'name': name,
            'alias': alias,
            'account_id': account_id,
            'relationship': relationship
        }
        
        # Publish success event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_success_event(
            event_type='BENEFICIARY_ADDED',
            data=response_data,
            correlation_id=correlation_id,
            source='crm',
            user_id=user_id
        )
        
        logger.info('Add beneficiary completed')
        
        return {
            'statusCode': 201,
            'body': {
                'message': 'Beneficiary added',
                'beneficiary_id': beneficiary_id,
                'correlation_id': correlation_id
            }
        }
        
    except CentliError as e:
        logger.error('Business error', error_code=e.error_code, error_message=e.message)
        
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='ADD_BENEFICIARY_FAILED',
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
            event_type='ADD_BENEFICIARY_FAILED',
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
