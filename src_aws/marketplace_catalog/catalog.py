"""
Marketplace - Catalog Query Lambda
Queries product catalog with filtering
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


PRODUCTS_TABLE = os.environ.get('PRODUCTS_TABLE', 'centli-products')
RETAILERS_TABLE = os.environ.get('RETAILERS_TABLE', 'centli-retailers')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')


def lambda_handler(event, context):
    """Lambda handler for product catalog query"""
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('marketplace-catalog', correlation_id)
    
    try:
        logger.info('Processing catalog query')
        
        detail = validate_event(event, ['user_id'])
        user_id = detail['user_id']
        category = detail.get('category')
        retailer_id = detail.get('retailer_id')
        limit = detail.get('limit', 20)
        
        logger.info('Query parameters', category=category, retailer_id=retailer_id)
        
        db_helper = DynamoDBHelper(PRODUCTS_TABLE)
        
        if retailer_id:
            # Query by retailer (GSI)
            products = db_helper.query(
                key_condition_expression='retailer_id = :retailer_id',
                expression_values={':retailer_id': retailer_id},
                index_name='retailer-index',
                limit=limit
            )
        else:
            # Scan all products (for demo, in production use better access pattern)
            from boto3.dynamodb.conditions import Attr
            products = db_helper.table.scan(Limit=limit).get('Items', [])
        
        # Filter by category if specified
        if category:
            products = [p for p in products if p.get('category') == category]
        
        logger.info('Products found', count=len(products))
        
        # Format products
        formatted_products = []
        for product in products:
            formatted_products.append({
                'product_id': product.get('product_id'),
                'name': product.get('name'),
                'description': product.get('description'),
                'price': float(product.get('price', 0)),
                'currency': product.get('currency', 'MXN'),
                'category': product.get('category'),
                'retailer_id': product.get('retailer_id'),
                'stock': int(product.get('stock', 0)),
                'image_url': product.get('image_url'),
                'benefits': product.get('benefits', [])
            })
        
        response_data = {
            'products': formatted_products,
            'count': len(formatted_products)
        }
        
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_success_event(
            event_type='CATALOG_RESPONSE',
            data=response_data,
            correlation_id=correlation_id,
            source='marketplace',
            user_id=user_id
        )
        
        logger.info('Catalog query completed')
        
        return {
            'statusCode': 200,
            'body': {
                'message': 'Catalog query completed',
                'count': len(formatted_products),
                'correlation_id': correlation_id
            }
        }
        
    except CentliError as e:
        logger.error('Business error', error_code=e.error_code, error_message=e.message)
        
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='CATALOG_QUERY_FAILED',
            error_message=e.message,
            error_code=e.error_code,
            correlation_id=correlation_id,
            source='marketplace',
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
            event_type='CATALOG_QUERY_FAILED',
            error_message='Internal server error',
            error_code='INTERNAL_ERROR',
            correlation_id=correlation_id,
            source='marketplace'
        )
        
        return {
            'statusCode': 500,
            'body': {
                'error': 'INTERNAL_ERROR',
                'message': 'Internal server error',
                'correlation_id': correlation_id
            }
        }
