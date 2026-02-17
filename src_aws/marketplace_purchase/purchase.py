"""
Marketplace - Purchase Lambda
Executes purchases with saga pattern and compensation logic
Handles: PURCHASE_REQUEST, PAYMENT_COMPLETED, PAYMENT_FAILED
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
    validate_positive_amount,
    CentliError,
    ProductNotFoundError,
    InsufficientStockError,
    python_to_dynamodb
)


PRODUCTS_TABLE = os.environ.get('PRODUCTS_TABLE', 'centli-products')
PURCHASES_TABLE = os.environ.get('PURCHASES_TABLE', 'centli-purchases')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')


def lambda_handler(event, context):
    """
    Lambda handler for purchase operations
    Handles multiple event types: PURCHASE_REQUEST, PAYMENT_COMPLETED, PAYMENT_FAILED
    """
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('marketplace-purchase', correlation_id)
    
    try:
        event_type = event.get('detail-type', '')
        logger.info('Processing purchase event', event_type=event_type)
        
        if event_type == 'PURCHASE_REQUEST':
            return handle_purchase_request(event, correlation_id, logger)
        elif event_type == 'PAYMENT_COMPLETED':
            return handle_payment_completed(event, correlation_id, logger)
        elif event_type == 'PAYMENT_FAILED':
            return handle_payment_failed(event, correlation_id, logger)
        else:
            raise CentliError(f'Unknown event type: {event_type}', 'UNKNOWN_EVENT_TYPE')
            
    except CentliError as e:
        logger.error('Business error', error_code=e.error_code, error_message=e.message)
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
        return {
            'statusCode': 500,
            'body': {
                'error': 'INTERNAL_ERROR',
                'message': 'Internal server error',
                'correlation_id': correlation_id
            }
        }


def handle_purchase_request(event, correlation_id, logger):
    """
    Handle PURCHASE_REQUEST event
    Steps:
    1. Validate product and stock
    2. Reserve inventory
    3. Publish PAYMENT_REQUEST event
    """
    detail = validate_event(event, ['user_id', 'product_id', 'quantity'])
    user_id = detail['user_id']
    product_id = detail['product_id']
    quantity = int(detail['quantity'])
    benefit_type = detail.get('benefit_type')  # MSI_6, CASHBACK_5, etc.
    
    validate_positive_amount(quantity, 'quantity')
    
    logger.info('Purchase request', product_id=product_id, quantity=quantity, benefit=benefit_type)
    
    # Get product
    products_helper = DynamoDBHelper(PRODUCTS_TABLE)
    products = products_helper.table.scan(
        FilterExpression='product_id = :pid',
        ExpressionAttributeValues={':pid': product_id}
    ).get('Items', [])
    
    if not products:
        raise ProductNotFoundError(product_id)
    
    product = products[0]
    available_stock = int(product.get('stock', 0))
    price = float(product.get('price', 0))
    
    # Check stock
    if available_stock < quantity:
        raise InsufficientStockError(product_id, available_stock, quantity)
    
    # Reserve inventory (update stock)
    new_stock = available_stock - quantity
    products_helper.table.update_item(
        Key={'product_id': product_id, 'retailer_id': product.get('retailer_id')},
        UpdateExpression='SET stock = :new_stock, reserved = reserved + :qty',
        ExpressionAttributeValues={
            ':new_stock': new_stock,
            ':qty': quantity
        }
    )
    
    logger.info('Inventory reserved', new_stock=new_stock)
    
    # Calculate total amount
    total_amount = price * quantity
    
    # Create pending purchase record
    purchase_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    purchase = {
        'user_id': user_id,
        'timestamp_purchase_id': f"{timestamp}#{purchase_id}",
        'purchase_id': purchase_id,
        'product_id': product_id,
        'retailer_id': product.get('retailer_id'),
        'quantity': quantity,
        'unit_price': python_to_dynamodb(price),
        'total_amount': python_to_dynamodb(total_amount),
        'benefit_applied': benefit_type,
        'status': 'pending',
        'correlation_id': correlation_id,
        'created_at': timestamp
    }
    
    purchases_helper = DynamoDBHelper(PURCHASES_TABLE)
    purchases_helper.put_item(purchase)
    
    logger.info('Purchase record created', purchase_id=purchase_id, status='pending')
    
    # Publish PAYMENT_REQUEST event to Core Banking
    eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
    eb_helper.publish_event(
        event_type='PAYMENT_REQUEST',
        data={
            'purchase_id': purchase_id,
            'product_id': product_id,
            'amount': total_amount,
            'currency': product.get('currency', 'MXN'),
            'description': f"Purchase: {product.get('name')}"
        },
        correlation_id=correlation_id,
        source='marketplace',
        user_id=user_id
    )
    
    logger.info('Payment request published')
    
    return {
        'statusCode': 200,
        'body': {
            'message': 'Purchase initiated, awaiting payment',
            'purchase_id': purchase_id,
            'status': 'pending',
            'correlation_id': correlation_id
        }
    }


def handle_payment_completed(event, correlation_id, logger):
    """
    Handle PAYMENT_COMPLETED event
    Steps:
    1. Update purchase status to completed
    2. Publish PURCHASE_CONFIRMED event
    """
    detail = validate_event(event, ['user_id', 'purchase_id'])
    user_id = detail['user_id']
    purchase_id = detail['purchase_id']
    transaction_id = detail.get('transaction_id')
    
    logger.info('Payment completed', purchase_id=purchase_id, transaction_id=transaction_id)
    
    # Update purchase status
    purchases_helper = DynamoDBHelper(PURCHASES_TABLE)
    
    # Find purchase (need to query by purchase_id)
    purchases = purchases_helper.table.scan(
        FilterExpression='purchase_id = :pid',
        ExpressionAttributeValues={':pid': purchase_id}
    ).get('Items', [])
    
    if not purchases:
        logger.warning('Purchase not found', purchase_id=purchase_id)
        return {
            'statusCode': 404,
            'body': {
                'error': 'PURCHASE_NOT_FOUND',
                'message': f'Purchase not found: {purchase_id}',
                'correlation_id': correlation_id
            }
        }
    
    purchase = purchases[0]
    
    # Update status to completed
    purchases_helper.table.update_item(
        Key={
            'user_id': purchase['user_id'],
            'timestamp_purchase_id': purchase['timestamp_purchase_id']
        },
        UpdateExpression='SET #status = :status, transaction_id = :txn_id, updated_at = :updated_at',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':status': 'completed',
            ':txn_id': transaction_id,
            ':updated_at': datetime.utcnow().isoformat() + 'Z'
        }
    )
    
    logger.info('Purchase completed', purchase_id=purchase_id)
    
    # Publish PURCHASE_CONFIRMED event
    eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
    eb_helper.publish_success_event(
        event_type='PURCHASE_CONFIRMED',
        data={
            'purchase_id': purchase_id,
            'product_id': purchase.get('product_id'),
            'quantity': purchase.get('quantity'),
            'total_amount': float(purchase.get('total_amount', 0)),
            'transaction_id': transaction_id,
            'status': 'completed'
        },
        correlation_id=correlation_id,
        source='marketplace',
        user_id=user_id
    )
    
    logger.info('Purchase confirmed event published')
    
    return {
        'statusCode': 200,
        'body': {
            'message': 'Purchase confirmed',
            'purchase_id': purchase_id,
            'status': 'completed',
            'correlation_id': correlation_id
        }
    }


def handle_payment_failed(event, correlation_id, logger):
    """
    Handle PAYMENT_FAILED event - COMPENSATION LOGIC
    Steps:
    1. Release reserved inventory
    2. Update purchase status to failed
    3. Publish PURCHASE_FAILED event
    """
    detail = validate_event(event, ['user_id', 'purchase_id'])
    user_id = detail['user_id']
    purchase_id = detail['purchase_id']
    error_message = detail.get('error', {}).get('message', 'Payment failed')
    
    logger.warning('Payment failed, starting compensation', purchase_id=purchase_id)
    
    # Find purchase
    purchases_helper = DynamoDBHelper(PURCHASES_TABLE)
    purchases = purchases_helper.table.scan(
        FilterExpression='purchase_id = :pid',
        ExpressionAttributeValues={':pid': purchase_id}
    ).get('Items', [])
    
    if not purchases:
        logger.warning('Purchase not found for compensation', purchase_id=purchase_id)
        return {
            'statusCode': 404,
            'body': {
                'error': 'PURCHASE_NOT_FOUND',
                'message': f'Purchase not found: {purchase_id}',
                'correlation_id': correlation_id
            }
        }
    
    purchase = purchases[0]
    product_id = purchase.get('product_id')
    quantity = int(purchase.get('quantity', 0))
    
    # COMPENSATION: Release reserved inventory
    products_helper = DynamoDBHelper(PRODUCTS_TABLE)
    products = products_helper.table.scan(
        FilterExpression='product_id = :pid',
        ExpressionAttributeValues={':pid': product_id}
    ).get('Items', [])
    
    if products:
        product = products[0]
        products_helper.table.update_item(
            Key={'product_id': product_id, 'retailer_id': product.get('retailer_id')},
            UpdateExpression='SET stock = stock + :qty, reserved = reserved - :qty',
            ExpressionAttributeValues={':qty': quantity}
        )
        logger.info('Inventory released (compensation)', product_id=product_id, quantity=quantity)
    
    # Update purchase status to failed
    purchases_helper.table.update_item(
        Key={
            'user_id': purchase['user_id'],
            'timestamp_purchase_id': purchase['timestamp_purchase_id']
        },
        UpdateExpression='SET #status = :status, error_message = :error, updated_at = :updated_at',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':status': 'failed',
            ':error': error_message,
            ':updated_at': datetime.utcnow().isoformat() + 'Z'
        }
    )
    
    logger.info('Purchase marked as failed', purchase_id=purchase_id)
    
    # Publish PURCHASE_FAILED event
    eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
    eb_helper.publish_error_event(
        event_type='PURCHASE_FAILED',
        error_message=error_message,
        error_code='PAYMENT_FAILED',
        correlation_id=correlation_id,
        source='marketplace',
        user_id=user_id,
        additional_data={
            'purchase_id': purchase_id,
            'product_id': product_id,
            'compensation_applied': True
        }
    )
    
    logger.info('Purchase failed event published with compensation')
    
    return {
        'statusCode': 200,
        'body': {
            'message': 'Purchase failed, compensation applied',
            'purchase_id': purchase_id,
            'status': 'failed',
            'compensation_applied': True,
            'correlation_id': correlation_id
        }
    }
