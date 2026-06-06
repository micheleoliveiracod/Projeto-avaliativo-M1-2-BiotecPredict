"""
Base Schema - Common configuration and base classes for all Pydantic schemas.

This module defines the base configuration used across all schemas in the API.
All schemas inherit from BaseSchema to ensure consistent behavior:
- from_attributes=True: Support SQLAlchemy model conversion
- json_encoders: Custom JSON encoding for special types
- validate_assignment: Validate on attribute assignment

Task 10: Criar Schema Base
- Definir configurações comuns (ConfigDict com from_attributes=True)
- Classe base para schemas
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """
    Base schema for all API schemas.
    
    Provides common configuration for all Pydantic models:
    - from_attributes=True: Convert SQLAlchemy models to Pydantic models
    - validate_assignment: Validate when assigning attributes
    - json_encoders: Custom JSON encoding for UUID and datetime
    
    All API schemas should inherit from this class to ensure consistency.
    
    Example:
        >>> class MySchema(BaseSchema):
        ...     name: str
        ...     value: int
        ...
        >>> schema = MySchema(name="test", value=42)
        >>> schema.model_dump_json()
        '{"name":"test","value":42}'
    """
    
    model_config = ConfigDict(
        from_attributes=True,  # Support SQLAlchemy model conversion
        validate_assignment=True,  # Validate on attribute assignment
        json_encoders={
            UUID: str,  # Encode UUID as string
            datetime: lambda v: v.isoformat() if v else None,  # ISO format for datetime
        },
        # Allow population by field name
        populate_by_name=True,
    )


class TimestampedSchema(BaseSchema):
    """
    Base schema with timestamp fields.
    
    Extends BaseSchema with common timestamp fields used in most API responses.
    
    Attributes:
        created_at (datetime): When the resource was created
        updated_at (Optional[datetime]): When the resource was last updated
    
    Example:
        >>> class UserSchema(TimestampedSchema):
        ...     name: str
    """
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class PaginatedSchema(BaseSchema):
    """
    Base schema for paginated responses.
    
    Provides common pagination fields for list endpoints.
    
    Attributes:
        total (int): Total number of items
        page (int): Current page number (1-indexed)
        limit (int): Items per page
        pages (int): Total number of pages
    
    Example:
        >>> class ItemListSchema(PaginatedSchema):
        ...     items: List[ItemSchema]
    """
    
    total: int = Field(..., ge=0, description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number (1-indexed)")
    limit: int = Field(..., ge=1, le=100, description="Items per page")
    pages: int = Field(..., ge=0, description="Total number of pages")
    
    @property
    def has_next(self) -> bool:
        """Check if there is a next page."""
        return self.page < self.pages
    
    @property
    def has_previous(self) -> bool:
        """Check if there is a previous page."""
        return self.page > 1
