"""
Core Banking - Balance Query Lambda
Queries account balance for a user
"""

import os
import sys

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import (
    StructuredLogger,
    extract_correlation_id,
    DynamoDBHelper,
    EventBridgeHelper,
    validate_event,
    validate_required_fields,
    CentliError,
    ResourceNotFoundError
)


# Environment variables
ACCOUNTS_TABLE = os.environ.get('ACCOUNTS_TABLE', 'centli-accounts')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')


def lambda_handler(event, context):
    """
    Lambda handler for balance query
    
    Args:
        event: EventBridge event with BALANCE_QUERY
        context: Lambda context
        
    Returns:
        dict: Response with statusCode and body
    """
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('core-banking-balance', correlation_id)
    
    try:
        logger.info('Processing balance query', event_type=event.get('detail-type'))
        
        # Validate and parse event
        detail = validate_event(event, ['user_id', 'account_id'])
        user_id = detail['user_id']
        account_id = detail['account_id']
        
        logger.info('Query parameters', user_id=user_id, account_id=account_id)
        
        # Query account from DynamoDB
        db_helper = DynamoDBHelper(ACCOUNTS_TABLE)
        account = db_helper.get_item(
            key={'user_id': user_id, 'account_id': account_id},
            consistent_read=True  # Strong consistency for balance
        )
        
        if not account:
            raise ResourceNotFoundError('Account', account_id)
        
        logger.info('Account found', account_type=account.get('account_type'))
        
        # Prepare response data
        response_data = {
            'account_id': account['account_id'],
            'account_type': account.get('account_type', 'checking'),
            'balance': float(account.get('balance', 0)),
            'currency': account.get('currency', 'MXN'),
            'status': account.get('status', 'active')
        }
        
        # Publish success event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_success_event(
            event_type='BALANCE_RESPONSE',
            data=response_data,
            correlation_id=correlation_id,
            source='core-banking',
            user_id=user_id
        )
        
        logger.info('Balance query completed successfully')
        
        return {
            'statusCode': 200,
            'body': {
                'message': 'Balance query completed',
                'correlation_id': correlation_id
            }
        }
        
    except CentliError as e:
        logger.error('Business error', error_code=e.error_code, error_message=e.message)
        
        # Publish error event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='BALANCE_QUERY_FAILED',
            error_message=e.message,
            error_code=e.error_code,
            correlation_id=correlation_id,
            source='core-banking',
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
        
        # Publish error event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='BALANCE_QUERY_FAILED',
            error_message='Internal server error',
            error_code='INTERNAL_ERROR',
            correlation_id=correlation_id,
            source='core-banking'
        )
        
        return {
            'statusCode': 500,
            'body': {
                'error': 'INTERNAL_ERROR',
                'message': 'Internal server error',
                'correlation_id': correlation_id
            }
        }
