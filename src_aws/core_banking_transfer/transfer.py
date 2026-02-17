"""
Core Banking - Transfer Lambda
Executes money transfers between accounts with optimistic locking
"""

import os
import sys
import uuid
from datetime import datetime
from decimal import Decimal

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import (
    StructuredLogger,
    extract_correlation_id,
    DynamoDBHelper,
    EventBridgeHelper,
    validate_event,
    validate_positive_amount,
    validate_account_id,
    CentliError,
    ResourceNotFoundError,
    InsufficientFundsError,
    ConcurrentUpdateError,
    python_to_dynamodb
)
from botocore.exceptions import ClientError


# Environment variables
ACCOUNTS_TABLE = os.environ.get('ACCOUNTS_TABLE', 'centli-accounts')
TRANSACTIONS_TABLE = os.environ.get('TRANSACTIONS_TABLE', 'centli-transactions')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')


def lambda_handler(event, context):
    """
    Lambda handler for money transfer
    
    Args:
        event: EventBridge event with TRANSFER_REQUEST
        context: Lambda context
        
    Returns:
        dict: Response with statusCode and body
    """
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('core-banking-transfer', correlation_id)
    
    try:
        logger.info('Processing transfer request', event_type=event.get('detail-type'))
        
        # Validate and parse event
        detail = validate_event(event, ['user_id', 'from_account', 'to_account', 'amount'])
        user_id = detail['user_id']
        from_account_id = detail['from_account']
        to_account_id = detail['to_account']
        amount = float(detail['amount'])
        currency = detail.get('currency', 'MXN')
        description = detail.get('description', 'Transfer')
        
        # Validate inputs
        validate_account_id(from_account_id)
        validate_account_id(to_account_id)
        validate_positive_amount(amount)
        
        if from_account_id == to_account_id:
            raise CentliError('Cannot transfer to same account', 'INVALID_TRANSFER')
        
        logger.info('Transfer parameters', 
                   from_account=from_account_id, 
                   to_account=to_account_id, 
                   amount=amount)
        
        # Execute transfer with retry for optimistic locking
        transaction_id = execute_transfer_with_retry(
            user_id=user_id,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            currency=currency,
            description=description,
            correlation_id=correlation_id,
            logger=logger
        )
        
        # Prepare response data
        response_data = {
            'transaction_id': transaction_id,
            'from_account': from_account_id,
            'to_account': to_account_id,
            'amount': amount,
            'currency': currency,
            'status': 'completed'
        }
        
        # Publish success event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_success_event(
            event_type='TRANSFER_COMPLETED',
            data=response_data,
            correlation_id=correlation_id,
            source='core-banking',
            user_id=user_id
        )
        
        logger.info('Transfer completed successfully', transaction_id=transaction_id)
        
        return {
            'statusCode': 200,
            'body': {
                'message': 'Transfer completed',
                'transaction_id': transaction_id,
                'correlation_id': correlation_id
            }
        }
        
    except CentliError as e:
        logger.error('Business error', error_code=e.error_code, error_message=e.message)
        
        # Publish error event
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='TRANSFER_FAILED',
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
            event_type='TRANSFER_FAILED',
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


def execute_transfer_with_retry(
    user_id: str,
    from_account_id: str,
    to_account_id: str,
    amount: float,
    currency: str,
    description: str,
    correlation_id: str,
    logger: StructuredLogger,
    max_retries: int = 3
) -> str:
    """
    Execute transfer with retry for optimistic locking conflicts
    
    Args:
        user_id: User ID
        from_account_id: Source account ID
        to_account_id: Destination account ID
        amount: Transfer amount
        currency: Currency code
        description: Transfer description
        correlation_id: Correlation ID
        logger: Logger instance
        max_retries: Maximum retry attempts
        
    Returns:
        Transaction ID
        
    Raises:
        InsufficientFundsError: If insufficient funds
        ConcurrentUpdateError: If max retries exceeded
    """
    accounts_helper = DynamoDBHelper(ACCOUNTS_TABLE)
    transactions_helper = DynamoDBHelper(TRANSACTIONS_TABLE)
    
    for attempt in range(max_retries):
        try:
            logger.info(f'Transfer attempt {attempt + 1}/{max_retries}')
            
            # Read from_account with strong consistency
            from_account = accounts_helper.get_item(
                key={'user_id': user_id, 'account_id': from_account_id},
                consistent_read=True
            )
            
            if not from_account:
                raise ResourceNotFoundError('Account', from_account_id)
            
            # Check sufficient funds
            current_balance = float(from_account.get('balance', 0))
            current_version = from_account.get('version', 0)
            
            if current_balance < amount:
                raise InsufficientFundsError(
                    f'Insufficient funds: balance={current_balance}, requested={amount}'
                )
            
            # Read to_account
            to_account = accounts_helper.get_item(
                key={'user_id': user_id, 'account_id': to_account_id},
                consistent_read=True
            )
            
            if not to_account:
                raise ResourceNotFoundError('Account', to_account_id)
            
            to_balance = float(to_account.get('balance', 0))
            to_version = to_account.get('version', 0)
            
            # Update from_account with optimistic locking
            new_from_balance = current_balance - amount
            accounts_helper.update_item(
                key={'user_id': user_id, 'account_id': from_account_id},
                update_expression='SET balance = :new_balance, version = :new_version, updated_at = :updated_at',
                expression_values={
                    ':new_balance': python_to_dynamodb(new_from_balance),
                    ':new_version': current_version + 1,
                    ':current_version': current_version,
                    ':updated_at': datetime.utcnow().isoformat() + 'Z'
                },
                condition_expression='version = :current_version'
            )
            
            # Update to_account with optimistic locking
            new_to_balance = to_balance + amount
            accounts_helper.update_item(
                key={'user_id': user_id, 'account_id': to_account_id},
                update_expression='SET balance = :new_balance, version = :new_version, updated_at = :updated_at',
                expression_values={
                    ':new_balance': python_to_dynamodb(new_to_balance),
                    ':new_version': to_version + 1,
                    ':current_version': to_version,
                    ':updated_at': datetime.utcnow().isoformat() + 'Z'
                },
                condition_expression='version = :current_version'
            )
            
            # Create transaction record
            transaction_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat() + 'Z'
            
            transaction = {
                'account_id': from_account_id,
                'timestamp_txn_id': f"{timestamp}#{transaction_id}",
                'user_id': user_id,
                'transaction_id': transaction_id,
                'type': 'transfer',
                'amount': python_to_dynamodb(amount),
                'currency': currency,
                'from_account': from_account_id,
                'to_account': to_account_id,
                'status': 'completed',
                'description': description,
                'correlation_id': correlation_id,
                'created_at': timestamp
            }
            
            transactions_helper.put_item(transaction)
            
            logger.info('Transfer executed successfully', 
                       transaction_id=transaction_id,
                       new_from_balance=new_from_balance,
                       new_to_balance=new_to_balance)
            
            return transaction_id
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                # Optimistic locking conflict - retry
                if attempt == max_retries - 1:
                    raise ConcurrentUpdateError('Max retries exceeded for concurrent update')
                
                logger.warning(f'Optimistic locking conflict, retrying...')
                import time
                time.sleep(0.1)  # Brief delay before retry
            else:
                raise
    
    raise ConcurrentUpdateError('Max retries exceeded')
