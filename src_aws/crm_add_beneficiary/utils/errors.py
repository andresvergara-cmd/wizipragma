"""
Custom exception classes for CENTLI
"""


class CentliError(Exception):
    """Base exception for CENTLI errors"""
    
    def __init__(self, message: str, error_code: str = 'CENTLI_ERROR'):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(CentliError):
    """Validation error"""
    
    def __init__(self, message: str):
        super().__init__(message, 'VALIDATION_ERROR')


class InsufficientFundsError(CentliError):
    """Insufficient funds error"""
    
    def __init__(self, message: str = 'Insufficient funds'):
        super().__init__(message, 'INSUFFICIENT_FUNDS')


class ResourceNotFoundError(CentliError):
    """Resource not found error"""
    
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} not found: {resource_id}"
        super().__init__(message, 'RESOURCE_NOT_FOUND')


class ConcurrentUpdateError(CentliError):
    """Concurrent update error (optimistic locking failure)"""
    
    def __init__(self, message: str = 'Concurrent update detected'):
        super().__init__(message, 'CONCURRENT_UPDATE')


class DuplicateRequestError(CentliError):
    """Duplicate request error (idempotency check failed)"""
    
    def __init__(self, request_id: str):
        message = f"Duplicate request: {request_id}"
        super().__init__(message, 'DUPLICATE_REQUEST')


class AliasNotFoundError(CentliError):
    """Alias not found error"""
    
    def __init__(self, alias: str):
        message = f"Alias not found: {alias}"
        super().__init__(message, 'ALIAS_NOT_FOUND')


class ProductNotFoundError(CentliError):
    """Product not found error"""
    
    def __init__(self, product_id: str):
        message = f"Product not found: {product_id}"
        super().__init__(message, 'PRODUCT_NOT_FOUND')


class InsufficientStockError(CentliError):
    """Insufficient stock error"""
    
    def __init__(self, product_id: str, available: int, requested: int):
        message = f"Insufficient stock for product {product_id}: available={available}, requested={requested}"
        super().__init__(message, 'INSUFFICIENT_STOCK')
