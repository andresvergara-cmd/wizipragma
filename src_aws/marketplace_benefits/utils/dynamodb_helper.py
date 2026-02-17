"""
DynamoDB helper functions with retry logic
"""

import time
from typing import Any, Callable, Dict, Optional
from decimal import Decimal
import boto3
from botocore.exceptions import ClientError


def retry_with_backoff(operation: Callable, max_retries: int = 3, base_delay: float = 0.1) -> Any:
    """
    Retry operation with exponential backoff
    
    Args:
        operation: Function to retry
        max_retries: Maximum number of retries
        base_delay: Base delay in seconds
        
    Returns:
        Operation result
        
    Raises:
        Exception: If all retries exhausted
    """
    for attempt in range(max_retries):
        try:
            return operation()
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            # Retry on throttling or transient errors
            if error_code in ['ProvisionedThroughputExceededException', 
                             'ThrottlingException',
                             'RequestLimitExceeded']:
                if attempt == max_retries - 1:
                    raise
                
                # Exponential backoff
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
            else:
                # Don't retry on other errors
                raise


class DynamoDBHelper:
    """
    Helper class for DynamoDB operations
    """
    
    def __init__(self, table_name: str):
        """
        Initialize DynamoDB helper
        
        Args:
            table_name: Name of DynamoDB table
        """
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        self.table_name = table_name
    
    def get_item(self, key: Dict[str, Any], consistent_read: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get item from DynamoDB with retry
        
        Args:
            key: Primary key
            consistent_read: Use strong consistency
            
        Returns:
            Item or None if not found
        """
        def operation():
            response = self.table.get_item(
                Key=key,
                ConsistentRead=consistent_read
            )
            return response.get('Item')
        
        return retry_with_backoff(operation)
    
    def put_item(self, item: Dict[str, Any]) -> None:
        """
        Put item to DynamoDB with retry
        
        Args:
            item: Item to put
        """
        def operation():
            self.table.put_item(Item=item)
        
        retry_with_backoff(operation)
    
    def update_item(
        self,
        key: Dict[str, Any],
        update_expression: str,
        expression_values: Dict[str, Any],
        condition_expression: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update item in DynamoDB with retry
        
        Args:
            key: Primary key
            update_expression: Update expression
            expression_values: Expression attribute values
            condition_expression: Condition expression (for optimistic locking)
            
        Returns:
            Updated attributes
            
        Raises:
            ClientError: If condition check fails
        """
        def operation():
            kwargs = {
                'Key': key,
                'UpdateExpression': update_expression,
                'ExpressionAttributeValues': expression_values,
                'ReturnValues': 'ALL_NEW'
            }
            
            if condition_expression:
                kwargs['ConditionExpression'] = condition_expression
            
            response = self.table.update_item(**kwargs)
            return response.get('Attributes', {})
        
        return retry_with_backoff(operation)
    
    def query(
        self,
        key_condition_expression: str,
        expression_values: Dict[str, Any],
        index_name: Optional[str] = None,
        scan_forward: bool = True,
        limit: Optional[int] = None,
        consistent_read: bool = False
    ) -> list:
        """
        Query DynamoDB table with retry
        
        Args:
            key_condition_expression: Key condition expression
            expression_values: Expression attribute values
            index_name: GSI name (optional)
            scan_forward: Sort order (True = ascending, False = descending)
            limit: Maximum items to return
            consistent_read: Use strong consistency
            
        Returns:
            List of items
        """
        def operation():
            kwargs = {
                'KeyConditionExpression': key_condition_expression,
                'ExpressionAttributeValues': expression_values,
                'ScanIndexForward': scan_forward,
                'ConsistentRead': consistent_read
            }
            
            if index_name:
                kwargs['IndexName'] = index_name
            
            if limit:
                kwargs['Limit'] = limit
            
            response = self.table.query(**kwargs)
            return response.get('Items', [])
        
        return retry_with_backoff(operation)
    
    def check_idempotency(self, request_id: str) -> bool:
        """
        Check if request has already been processed
        
        Args:
            request_id: Request ID
            
        Returns:
            True if duplicate, False otherwise
        """
        item = self.get_item(
            key={'request_id': request_id},
            consistent_read=True
        )
        return item is not None
    
    def store_idempotency(self, request_id: str, result: Any, ttl_hours: int = 24) -> None:
        """
        Store request ID for idempotency
        
        Args:
            request_id: Request ID
            result: Operation result
            ttl_hours: TTL in hours
        """
        import time
        from datetime import datetime
        
        item = {
            'request_id': request_id,
            'result': result,
            'processed_at': datetime.utcnow().isoformat() + 'Z',
            'ttl': int(time.time()) + (ttl_hours * 3600)
        }
        
        self.put_item(item)


def python_to_dynamodb(obj: Any) -> Any:
    """
    Convert Python types to DynamoDB types
    
    Args:
        obj: Python object
        
    Returns:
        DynamoDB-compatible object
    """
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: python_to_dynamodb(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [python_to_dynamodb(item) for item in obj]
    else:
        return obj


def dynamodb_to_python(obj: Any) -> Any:
    """
    Convert DynamoDB types to Python types
    
    Args:
        obj: DynamoDB object
        
    Returns:
        Python object
    """
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: dynamodb_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [dynamodb_to_python(item) for item in obj]
    else:
        return obj
