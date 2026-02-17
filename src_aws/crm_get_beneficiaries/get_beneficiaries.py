"""
CRM - Get Beneficiaries Lambda
Lists all beneficiaries for a user
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
    CentliError
)


BENEFICIARIES_TABLE = os.environ.get('BENEFICIARIES_TABLE', 'centli-beneficiaries')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')


def lambda_handler(event, context):
    """Lambda handler for get beneficiaries"""
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('crm-get-beneficiaries', correlation_id)
    
    try:
        logger.info('Processing get beneficiaries request')
        
        detail = validate_event(event, ['user_id'])
        user_id = detail['user_id']
        
        logger.info('Getting beneficiaries', user_id=user_id)
        
        # Query beneficiaries by user_id
        db_helper = DynamoDBHelper(BENEFICIARIES_TABLE)
        beneficiaries = db_helper.query(
            key_condition_expression='user_id = :user_id',
            expression_values={':user_id': user_id}
        )
        
        logger.info('Beneficiaries found', count=len(beneficiaries))
        
        # Format beneficiaries
        formatted_beneficiaries = []
        for beneficiary in beneficiaries:
            formatted_beneficiaries.append({
                'beneficiary_id': beneficiary.get('beneficiary_id'),
                'name': beneficiary.get('name'),
                'alias': beneficiary.get('alias'),
                'account_id': beneficiary.get('account_id'),
                'relationship': beneficiary.get('relationship'),
                'created_at': beneficiary.get('created_at')
            })
        
        response_data = {
            'beneficiaries': formatted_beneficiaries,
            'count': len(formatted_beneficiaries)
        }
        
        # Publish success event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_success_event(
            event_type='BENEFICIARIES_RESPONSE',
            data=response_data,
            correlation_id=correlation_id,
            source='crm',
            user_id=user_id
        )
        
        logger.info('Get beneficiaries completed')
        
        return {
            'statusCode': 200,
            'body': {
                'message': 'Beneficiaries retrieved',
                'count': len(formatted_beneficiaries),
                'correlation_id': correlation_id
            }
        }
        
    except CentliError as e:
        logger.error('Business error', error_code=e.error_code, error_message=e.message)
        
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='BENEFICIARIES_QUERY_FAILED',
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
            event_type='BENEFICIARIES_QUERY_FAILED',
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
