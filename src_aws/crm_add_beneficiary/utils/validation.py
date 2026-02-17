"""
Input validation utilities
"""

from typing import Any, Dict, List
from .errors import ValidationError


def validate_event(event: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
    """
    Validate EventBridge event structure
    
    Args:
        event: EventBridge event
        required_fields: Required fields in event detail
        
    Returns:
        Event detail
        
    Raises:
        ValidationError: If validation fails
    """
    # Check event has detail
    if 'detail' not in event:
        raise ValidationError("Event missing 'detail' field")
    
    detail = event['detail']
    
    # Check required fields
    validate_required_fields(detail, required_fields)
    
    return detail


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """
    Validate required fields are present
    
    Args:
        data: Data dictionary
        required_fields: List of required field names
        
    Raises:
        ValidationError: If any required field is missing
    """
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")


def validate_positive_amount(amount: float, field_name: str = 'amount') -> None:
    """
    Validate amount is positive
    
    Args:
        amount: Amount to validate
        field_name: Field name for error message
        
    Raises:
        ValidationError: If amount is not positive
    """
    if not isinstance(amount, (int, float)):
        raise ValidationError(f"{field_name} must be a number")
    
    if amount <= 0:
        raise ValidationError(f"{field_name} must be positive")


def validate_currency(currency: str) -> None:
    """
    Validate currency code
    
    Args:
        currency: Currency code
        
    Raises:
        ValidationError: If currency is invalid
    """
    valid_currencies = ['MXN', 'USD']
    
    if currency not in valid_currencies:
        raise ValidationError(f"Invalid currency: {currency}. Must be one of {valid_currencies}")


def validate_account_id(account_id: str) -> None:
    """
    Validate account ID format
    
    Args:
        account_id: Account ID
        
    Raises:
        ValidationError: If account ID is invalid
    """
    if not account_id or not isinstance(account_id, str):
        raise ValidationError("Invalid account_id")
    
    if len(account_id) < 3:
        raise ValidationError("account_id too short")


def validate_user_id(user_id: str) -> None:
    """
    Validate user ID format
    
    Args:
        user_id: User ID
        
    Raises:
        ValidationError: If user ID is invalid
    """
    if not user_id or not isinstance(user_id, str):
        raise ValidationError("Invalid user_id")
    
    if len(user_id) < 3:
        raise ValidationError("user_id too short")
