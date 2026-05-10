class ProcessingError(Exception):
    """Base exception for all processing-related errors."""
    pass

class DataCleaningError(ProcessingError):
    """Raised when data cleaning fails (e.g., empty dataframe after cleaning)."""
    pass

class FeatureEngineeringError(ProcessingError):
    """Raised when feature generation fails."""
    pass

class MetricsStorageError(ProcessingError):
    """Raised when saving processed metrics fails."""
    pass
