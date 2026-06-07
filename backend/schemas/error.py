"""
Error Response Schema - Pydantic models for error responses.

This module defines standardized error response schemas used throughout the API.
All errors follow a consistent format with error message, details, timestamp,
and request path for debugging.

Task 16: Implementar ErrorResponseSchema
- Criar schema padronizado para erros
- error, details, timestamp, path
"""

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import Field

from backend.schemas.base import BaseSchema


class ErrorDetail(BaseSchema):
    """
    Schema for individual error detail.
    
    Represents a single error detail with field name, error message,
    and optional additional information.
    
    Attributes:
        field (str): Name of the field that caused the error
        message (str): Error message
        value (Optional[Any]): The value that caused the error
        code (Optional[str]): Error code for programmatic handling
    
    Example:
        >>> detail = ErrorDetail(
        ...     field="temperature",
        ...     message="Temperature must be between 20 and 45°C",
        ...     value=50.0,
        ...     code="RANGE_ERROR"
        ... )
    """
    
    field: str = Field(
        ...,
        description="Name of the field that caused the error",
    )
    
    message: str = Field(
        ...,
        description="Error message",
    )
    
    value: Optional[Any] = Field(
        default=None,
        description="The value that caused the error",
    )
    
    code: Optional[str] = Field(
        default=None,
        description="Error code for programmatic handling",
    )


class ErrorResponse(BaseSchema):
    """
    Schema for standardized error responses.
    
    Used for all error responses from the API. Provides consistent error
    information including error message, details, timestamp, and request path.
    
    Attributes:
        error (str): Main error message
        details (Optional[List[ErrorDetail]]): List of detailed errors
        timestamp (datetime): When the error occurred
        path (str): Request path that caused the error
        status_code (int): HTTP status code
    
    Example:
        >>> error = ErrorResponse(
        ...     error="Validation error",
        ...     details=[
        ...         ErrorDetail(
        ...             field="temperature",
        ...             message="Temperature must be between 20 and 45°C",
        ...             value=50.0,
        ...             code="RANGE_ERROR"
        ...         )
        ...     ],
        ...     timestamp=datetime.utcnow(),
        ...     path="/api/v1/upload",
        ...     status_code=422
        ... )
        >>> error.model_dump_json()
        '{...}'
    """
    
    error: str = Field(
        ...,
        description="Main error message",
    )
    
    details: Optional[List[ErrorDetail]] = Field(
        default=None,
        description="List of detailed errors",
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the error occurred",
    )
    
    path: str = Field(
        ...,
        description="Request path that caused the error",
    )
    
    status_code: int = Field(
        ...,
        ge=400,
        le=599,
        description="HTTP status code",
    )
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "error": "Validation error",
                "details": [
                    {
                        "field": "temperature",
                        "message": "Temperature must be between 20 and 45°C",
                        "value": 50.0,
                        "code": "RANGE_ERROR",
                    }
                ],
                "timestamp": "2026-05-27T14:35:22",
                "path": "/api/v1/upload",
                "status_code": 422,
            }
        }


class ValidationErrorResponse(ErrorResponse):
    """
    Schema for validation error responses.
    
    Specialized error response for validation errors (HTTP 422).
    
    Attributes:
        error (str): Always "Validation error"
        details (List[ErrorDetail]): List of validation errors
        timestamp (datetime): When the error occurred
        path (str): Request path
        status_code (int): Always 422
    
    Example:
        >>> error = ValidationErrorResponse(
        ...     error="Validation error",
        ...     details=[...],
        ...     timestamp=datetime.utcnow(),
        ...     path="/api/v1/upload",
        ...     status_code=422
        ... )
    """
    
    error: str = Field(
        default="Validation error",
        description="Error type",
    )
    
    details: List[ErrorDetail] = Field(
        ...,
        description="List of validation errors",
    )
    
    status_code: int = Field(
        default=422,
        description="HTTP status code",
    )


class NotFoundErrorResponse(ErrorResponse):
    """
    Schema for not found error responses.
    
    Specialized error response for resource not found errors (HTTP 404).
    
    Attributes:
        error (str): Error message
        timestamp (datetime): When the error occurred
        path (str): Request path
        status_code (int): Always 404
    
    Example:
        >>> error = NotFoundErrorResponse(
        ...     error="Batch not found",
        ...     timestamp=datetime.utcnow(),
        ...     path="/api/v1/batch/550e8400-e29b-41d4-a716-446655440000",
        ...     status_code=404
        ... )
    """
    
    status_code: int = Field(
        default=404,
        description="HTTP status code",
    )


class BadRequestErrorResponse(ErrorResponse):
    """
    Schema for bad request error responses.
    
    Specialized error response for bad request errors (HTTP 400).
    
    Attributes:
        error (str): Error message
        details (Optional[List[ErrorDetail]]): Optional error details
        timestamp (datetime): When the error occurred
        path (str): Request path
        status_code (int): Always 400
    
    Example:
        >>> error = BadRequestErrorResponse(
        ...     error="Invalid CSV file",
        ...     details=[
        ...         ErrorDetail(
        ...             field="file",
        ...             message="File is empty",
        ...             code="EMPTY_FILE"
        ...         )
        ...     ],
        ...     timestamp=datetime.utcnow(),
        ...     path="/api/v1/upload",
        ...     status_code=400
        ... )
    """
    
    status_code: int = Field(
        default=400,
        description="HTTP status code",
    )


class InternalServerErrorResponse(ErrorResponse):
    """
    Schema for internal server error responses.
    
    Specialized error response for internal server errors (HTTP 500).
    
    Attributes:
        error (str): Generic error message (never exposes internal details)
        timestamp (datetime): When the error occurred
        path (str): Request path
        status_code (int): Always 500
    
    Example:
        >>> error = InternalServerErrorResponse(
        ...     error="Internal server error",
        ...     timestamp=datetime.utcnow(),
        ...     path="/api/v1/upload",
        ...     status_code=500
        ... )
    """
    
    error: str = Field(
        default="Internal server error",
        description="Generic error message",
    )
    
    status_code: int = Field(
        default=500,
        description="HTTP status code",
    )


class ServiceUnavailableErrorResponse(ErrorResponse):
    """
    Schema for service unavailable error responses.
    
    Specialized error response for service unavailable errors (HTTP 503).
    Used when database or other critical services are unavailable.
    
    Attributes:
        error (str): Error message
        timestamp (datetime): When the error occurred
        path (str): Request path
        status_code (int): Always 503
    
    Example:
        >>> error = ServiceUnavailableErrorResponse(
        ...     error="Database unavailable",
        ...     timestamp=datetime.utcnow(),
        ...     path="/api/v1/batches",
        ...     status_code=503
        ... )
    """
    
    status_code: int = Field(
        default=503,
        description="HTTP status code",
    )
