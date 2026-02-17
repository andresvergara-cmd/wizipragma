"""
Marketplace - Benefits Calculation Lambda
Calculates product benefits (MSI, cashback, points)
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
    ProductNotFoundError
)


PRODUCTS_TABLE = os.environ.get('PRODUCTS_TABLE', 'centli-products')
EVENT_BUS_NAME = os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')


def lambda_handler(event, context):
    """Lambda handler for benefits calculation"""
    correlation_id = extract_correlation_id(event)
    logger = StructuredLogger('marketplace-benefits', correlation_id)
    
    try:
        logger.info('Processing benefits query')
        
        detail = validate_event(event, ['user_id', 'product_id'])
        user_id = detail['user_id']
        product_id = detail['product_id']
        
        logger.info('Query parameters', product_id=product_id)
        
        # Get product
        db_helper = DynamoDBHelper(PRODUCTS_TABLE)
        # For simplicity, scan for product (in production, use better key design)
        products = db_helper.table.scan(
            FilterExpression='product_id = :pid',
            ExpressionAttributeValues={':pid': product_id}
        ).get('Items', [])
        
        if not products:
            raise ProductNotFoundError(product_id)
        
        product = products[0]
        price = float(product.get('price', 0))
        benefits = product.get('benefits', [])
        
        # Calculate benefit options
        benefit_options = []
        
        for benefit in benefits:
            if benefit == 'MSI_3':
                benefit_options.append({
                    'type': 'MSI',
                    'months': 3,
                    'monthly_payment': round(price / 3, 2),
                    'total': price,
                    'interest': 0
                })
            elif benefit == 'MSI_6':
                benefit_options.append({
                    'type': 'MSI',
                    'months': 6,
                    'monthly_payment': round(price / 6, 2),
                    'total': price,
                    'interest': 0
                })
            elif benefit == 'MSI_12':
                benefit_options.append({
                    'type': 'MSI',
                    'months': 12,
                    'monthly_payment': round(price / 12, 2),
                    'total': price,
                    'interest': 0
                })
            elif benefit == 'CASHBACK_5':
                benefit_options.append({
                    'type': 'CASHBACK',
                    'percentage': 5,
                    'cashback_amount': round(price * 0.05, 2),
                    'final_price': round(price * 0.95, 2)
                })
            elif benefit == 'POINTS_2X':
                benefit_options.append({
                    'type': 'POINTS',
                    'multiplier': 2,
                    'points_earned': int(price * 2)
                })
        
        logger.info('Benefits calculated', options_count=len(benefit_options))
        
        response_data = {
            'product_id': product_id,
            'price': price,
            'currency': product.get('currency', 'MXN'),
            'benefit_options': benefit_options
        }
        
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_success_event(
            event_type='BENEFITS_RESPONSE',
            data=response_data,
            correlation_id=correlation_id,
            source='marketplace',
            user_id=user_id
        )
        
        logger.info('Benefits query completed')
        
        return {
            'statusCode': 200,
            'body': {
                'message': 'Benefits calculated',
                'options_count': len(benefit_options),
                'correlation_id': correlation_id
            }
        }
        
    except CentliError as e:
        logger.error('Business error', error_code=e.error_code, error_message=e.message)
        
        eb_helper = EventBridgeHelper(EVENT_BUS_NAME)
        eb_helper.publish_error_event(
            event_type='BENEFITS_QUERY_FAILED',
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
            event_type='BENEFITS_QUERY_FAILED',
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
