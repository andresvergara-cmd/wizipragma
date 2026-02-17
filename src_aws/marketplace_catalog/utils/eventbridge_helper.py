"""
EventBridge helper for publishing events
"""

import json
import os
from datetime import datetime
from typing import Any, Dict
import boto3
from botocore.exceptions import ClientError


class EventBridgeHelper:
    """
    Helper class for publishing events to EventBridge
    """
    
    def __init__(self, event_bus_name: str = None):
        """
        Initialize EventBridge helper
        
        Args:
            event_bus_name: Name of EventBridge event bus
        """
        self.eventbridge = boto3.client('events')
        self.event_bus_name = event_bus_name or os.environ.get('EVENT_BUS_NAME', 'centli-event-bus')
    
    def publish_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        correlation_id: str,
        source: str,
        user_id: str = None
    ) -> bool:
        """
        Publish event to EventBridge
        
        Args:
            event_type: Event type (e.g., TRANSFER_COMPLETED)
            data: Event data payload
            correlation_id: Correlation ID for tracking
            source: Event source (e.g., core-banking)
            user_id: User ID (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Build event detail
            detail = {
                'version': '1.0',
                'event_type': event_type,
                'correlation_id': correlation_id,
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'source': source,
                'data': data
            }
            
            if user_id:
                detail['user_id'] = user_id
            
            # Publish to EventBridge
            response = self.eventbridge.put_events(
                Entries=[
                    {
                        'Source': f'centli.{source}',
                        'DetailType': event_type,
                        'Detail': json.dumps(detail),
                        'EventBusName': self.event_bus_name
                    }
                ]
            )
            
            # Check for failures
            if response['FailedEntryCount'] > 0:
                print(f"Failed to publish event: {response['Entries']}")
                return False
            
            return True
            
        except ClientError as e:
            print(f"Error publishing event: {str(e)}")
            return False
    
    def publish_success_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        correlation_id: str,
        source: str,
        user_id: str = None
    ) -> bool:
        """
        Publish success event
        
        Args:
            event_type: Event type (e.g., TRANSFER_COMPLETED)
            data: Event data payload
            correlation_id: Correlation ID
            source: Event source
            user_id: User ID (optional)
            
        Returns:
            True if successful
        """
        return self.publish_event(
            event_type=event_type,
            data=data,
            correlation_id=correlation_id,
            source=source,
            user_id=user_id
        )
    
    def publish_error_event(
        self,
        event_type: str,
        error_message: str,
        error_code: str,
        correlation_id: str,
        source: str,
        user_id: str = None,
        additional_data: Dict[str, Any] = None
    ) -> bool:
        """
        Publish error event
        
        Args:
            event_type: Event type (e.g., TRANSFER_FAILED)
            error_message: Error message
            error_code: Error code
            correlation_id: Correlation ID
            source: Event source
            user_id: User ID (optional)
            additional_data: Additional error data
            
        Returns:
            True if successful
        """
        data = {
            'error': {
                'code': error_code,
                'message': error_message,
                'correlation_id': correlation_id
            }
        }
        
        if additional_data:
            data.update(additional_data)
        
        return self.publish_event(
            event_type=event_type,
            data=data,
            correlation_id=correlation_id,
            source=source,
            user_id=user_id
        )
