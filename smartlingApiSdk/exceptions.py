class SmartlingException(Exception):
    """Base exception for Smartling API SDK errors."""
    pass

class SmartlingAuthError(SmartlingException):
    """Raised when authentication fails."""
    pass

class SmartlingAPIError(SmartlingException):
    """Raised for general Smartling API errors (non-2xx status codes)."""
    def __init__(self, message, status_code, request_id=None, errors=None):
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id
        self.errors = errors or []

class SmartlingClientError(SmartlingAPIError):
    """Raised for 4xx client errors."""
    pass

class SmartlingServerError(SmartlingAPIError):
    """Raised for 5xx server errors."""
    pass

class SmartlingTimeoutError(SmartlingException):
    """Raised when a request times out."""
    pass

class SmartlingConnectionError(SmartlingException):
    """Raised for network-related errors (e.g., DNS failure, refused connection)."""
    pass
