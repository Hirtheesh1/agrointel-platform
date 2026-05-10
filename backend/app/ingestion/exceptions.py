class IngestionError(Exception):
    """Base exception for all ingestion-related errors."""
    pass

class APIClientError(IngestionError):
    """Raised when an external API call fails (HTTP errors, timeouts)."""
    pass

class DataValidationError(IngestionError):
    """Raised when the fetched data fails validation schemas."""
    pass

class DataNormalizationError(IngestionError):
    """Raised when validating data cannot be normalized into the internal schema."""
    pass
