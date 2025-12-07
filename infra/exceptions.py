"""
Custom exception classes for the SQL Practice Platform.
"""

class SQLPracticeError(Exception):
    """Base exception for SQL Practice Platform errors."""
    pass


class ConfigurationError(SQLPracticeError):
    """Raised when there's an issue with configuration files."""
    pass


class DataGenerationError(SQLPracticeError):
    """Raised when data generation fails."""
    pass


class ValidationError(SQLPracticeError):
    """Raised when input validation fails."""
    pass


class DatabaseError(SQLPracticeError):
    """Raised when database operations fail."""
    pass


class FileIOError(SQLPracticeError):
    """Raised when file I/O operations fail."""
    pass


class LoggingError(SQLPracticeError):
    """Raised when logging setup fails."""
    pass