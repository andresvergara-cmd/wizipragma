"""
Structured logging with PII masking for CENTLI
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, Optional


class StructuredLogger:
    """
    Structured JSON logger with PII masking and correlation ID tracking
    """
    
    def __init__(self, lambda_name: str, correlation_id: str):
        """
        Initialize logger
        
        Args:
            lambda_name: Name of the Lambda function
            correlation_id: Correlation ID for request tracking
        """
        self.lambda_name = lambda_name
        self.correlation_id = correlation_id
    
    def _mask_pii(self, data: Any) -> Any:
        """
        Mask sensitive PII fields in log data
        
        Args:
            data: Data to mask
            
        Returns:
            Masked data
        """
        if isinstance(data, dict):
            masked = {}
            for key, value in data.items():
                if key in ['account_number', 'balance', 'amount']:
                    masked[key] = '***'
                elif key == 'account_id':
                    # Show last 4 characters only
                    if isinstance(value, str) and len(value) > 4:
                        masked[key] = f"***{value[-4:]}"
                    else:
                        masked[key] = '***'
                else:
                    masked[key] = self._mask_pii(value)
            return masked
        elif isinstance(data, list):
            return [self._mask_pii(item) for item in data]
        else:
            return data
    
    def _log(self, level: str, message: str, **kwargs):
        """
        Internal log method
        
        Args:
            level: Log level (INFO, ERROR, WARNING, DEBUG)
            message: Log message
            **kwargs: Additional fields to log
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': level,
            'lambda': self.lambda_name,
            'correlation_id': self.correlation_id,
            'message': message
        }
        
        # Add additional fields with PII masking
        if kwargs:
            log_entry.update(self._mask_pii(kwargs))
        
        print(json.dumps(log_entry))
    
    def info(self, message: str, **kwargs):
        """Log INFO level message"""
        self._log('INFO', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log ERROR level message"""
        self._log('ERROR', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log WARNING level message"""
        self._log('WARNING', message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log DEBUG level message"""
        self._log('DEBUG', message, **kwargs)


def extract_correlation_id(event: Dict[str, Any]) -> str:
    """
    Extract correlation ID from event or generate new one
    
    Args:
        event: EventBridge event
        
    Returns:
        Correlation ID
    """
    import uuid
    
    # Try to extract from event detail
    if 'detail' in event and isinstance(event['detail'], dict):
        correlation_id = event['detail'].get('correlation_id')
        if correlation_id:
            return correlation_id
    
    # Generate new correlation ID
    return str(uuid.uuid4())
