"""
Core Banking - Transactions Query Lambda
Queries transaction history for a user or account
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
    CentliError
)


# Environment variables
TRANSACTIONS_TABLE = os.environ.get('TRANSACTIONS_TABLE', 'centli-transactions')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')


def lambda_handler(event, context):
    """
    Lambda handler for transaction history query
    
    Args:
        event: EventBridge event with TRANSACTIONS_QUERY
        context: Lambda context
        
    Returns:
        dict: Response with statusCode and body
    """
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('core-banking-transactions', correlation_id)
    
    try:
        logger.info('Processing transactions query', event_type=event.get('detail-type'))
        
        # Validate and parse event
        detail = validate_event(event, ['user_id'])
        user_id = detail['user_id']
        account_id = detail.get('account_id')  # Optional: filter by account
        limit = detail.get('limit', 20)  # Default 20 transactions
        
        logger.info('Query parameters', user_id=user_id, account_id=account_id, limit=limit)
        
        # Query transactions from DynamoDB
        db_helper = DynamoDBHelper(TRANSACTIONS_TABLE)
        
        if account_id:
            # Query by account_id (primary key)
            transactions = db_helper.query(
                key_condition_expression='account_id = :account_id',
                expression_values={':account_id': account_id},
                scan_forward=False,  # Descending order (newest first)
                limit=limit
            )
        else:
            # Query by user_id (GSI)
            transactions = db_helper.query(
                key_condition_expression='user_id = :user_id',
                expression_values={':user_id': user_id},
                index_name='user-index',
                scan_forward=False,  # Descending order (newest first)
                limit=limit
            )
        
        logger.info('Transactions found', count=len(transactions))
        
        # Format transactions for response
        formatted_transactions = []
        for txn in transactions:
            formatted_transactions.append({
                'transaction_id': txn.get('transaction_id'),
                'type': txn.get('type'),
                'amount': float(txn.get('amount', 0)),
                'currency': txn.get('currency', 'MXN'),
                'from_account': txn.get('from_account'),
                'to_account': txn.get('to_account'),
                'status': txn.get('status'),
                'description': txn.get('description'),
                'created_at': txn.get('created_at')
            })
        
        # Prepare response data
        response_data = {
            'user_id': user_id,
            'account_id': account_id,
            'transactions': formatted_transactions,
            'count': len(formatted_transactions)
        }
        
        # Publish success event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_success_event(
            event_type='TRANSACTIONS_RESPONSE',
            data=response_data,
            correlation_id=correlation_id,
            source='core-banking',
            user_id=user_id
        )
        
        logger.info('Transactions query completed successfully')
        
        return {
            'statusCode': 200,
            'body': {
                'message': 'Transactions query completed',
                'count': len(formatted_transactions),
                'correlation_id': correlation_id
            }
        }
        
    except CentliError as e:
        logger.error('Business error', error_code=e.error_code, error_message=e.message)
        
        # Publish error event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='TRANSACTIONS_QUERY_FAILED',
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
            event_type='TRANSACTIONS_QUERY_FAILED',
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
