"""
Unit tests for BaseSchema and related base schema classes.

Tests cover:
- BaseSchema configuration (from_attributes, validate_assignment)
- JSON encoding for UUID and datetime
- TimestampedSchema with timestamp fields
- PaginatedSchema with pagination fields
- model_dump() with None handling
- Custom validators
- Round-trip serialization/deserialization

Task 10: Criar Schema Base - Testes Unitários
"""

from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel, Field, ValidationError

from backend.schemas.base import BaseSchema, PaginatedSchema, TimestampedSchema


class TestBaseSchema:
    """Test BaseSchema configuration and behavior."""

    def test_base_schema_from_attributes_enabled(self):
        """Test that from_attributes=True allows SQLAlchemy model conversion."""
        
        class SimpleSchema(BaseSchema):
            name: str
            value: int
        
        # Create a mock SQLAlchemy-like object
        class MockModel:
            def __init__(self):
                self.name = "test"
                self.value = 42
        
        mock = MockModel()
        schema = SimpleSchema.model_validate(mock)
        
        assert schema.name == "test"
        assert schema.value == 42

    def test_base_schema_validate_assignment(self):
        """Test that validate_assignment validates on attribute assignment."""
        
        class SimpleSchema(BaseSchema):
            value: int
        
        schema = SimpleSchema(value=42)
        
        # Assignment should validate
        with pytest.raises(ValidationError):
            schema.value = "not an int"

    def test_base_schema_uuid_encoding(self):
        """Test that UUID is encoded as string in JSON."""
        
        class SchemaWithUUID(BaseSchema):
            id: UUID
        
        test_uuid = uuid4()
        schema = SchemaWithUUID(id=test_uuid)
        
        # UUID should be encoded as string
        json_data = schema.model_dump_json()
        assert str(test_uuid) in json_data
        assert json_data.count('"') >= 2  # At least opening and closing quotes

    def test_base_schema_datetime_encoding(self):
        """Test that datetime is encoded in ISO format."""
        
        class SchemaWithDatetime(BaseSchema):
            timestamp: datetime
        
        now = datetime.utcnow()
        schema = SchemaWithDatetime(timestamp=now)
        
        # Datetime should be encoded in ISO format
        json_data = schema.model_dump_json()
        assert now.isoformat() in json_data

    def test_base_schema_datetime_none_handling(self):
        """Test that None datetime values are handled correctly."""
        
        class SchemaWithOptionalDatetime(BaseSchema):
            timestamp: Optional[datetime] = None
        
        schema = SchemaWithOptionalDatetime(timestamp=None)
        json_data = schema.model_dump_json()
        
        # None should be encoded as null
        assert "null" in json_data

    def test_base_schema_populate_by_name(self):
        """Test that populate_by_name allows field name population."""
        
        class SchemaWithAlias(BaseSchema):
            user_name: str = Field(alias="userName")
        
        # Should accept both field name and alias
        schema1 = SchemaWithAlias(user_name="john")
        assert schema1.user_name == "john"
        
        schema2 = SchemaWithAlias(userName="jane")
        assert schema2.user_name == "jane"

    def test_base_schema_model_dump_with_none(self):
        """Test model_dump() with None values."""
        
        class SchemaWithOptional(BaseSchema):
            name: str
            description: Optional[str] = None
        
        schema = SchemaWithOptional(name="test", description=None)
        dumped = schema.model_dump()
        
        assert dumped["name"] == "test"
        assert dumped["description"] is None

    def test_base_schema_model_dump_exclude_none(self):
        """Test model_dump(exclude_none=True) excludes None values."""
        
        class SchemaWithOptional(BaseSchema):
            name: str
            description: Optional[str] = None
        
        schema = SchemaWithOptional(name="test", description=None)
        dumped = schema.model_dump(exclude_none=True)
        
        assert dumped["name"] == "test"
        assert "description" not in dumped

    def test_base_schema_round_trip_serialization(self):
        """Test round-trip serialization/deserialization."""
        
        class ComplexSchema(BaseSchema):
            id: UUID
            name: str
            timestamp: datetime
            value: Optional[int] = None
        
        original = ComplexSchema(
            id=uuid4(),
            name="test",
            timestamp=datetime.utcnow(),
            value=42
        )
        
        # Serialize to dict
        dumped = original.model_dump()
        
        # Deserialize back
        restored = ComplexSchema(**dumped)
        
        assert restored.id == original.id
        assert restored.name == original.name
        assert restored.value == original.value

    def test_base_schema_json_round_trip(self):
        """Test round-trip through JSON."""
        
        class SchemaWithUUID(BaseSchema):
            id: UUID
            name: str
        
        original = SchemaWithUUID(id=uuid4(), name="test")
        
        # Serialize to JSON
        json_str = original.model_dump_json()
        
        # Deserialize from JSON
        restored = SchemaWithUUID.model_validate_json(json_str)
        
        assert restored.id == original.id
        assert restored.name == original.name


class TestTimestampedSchema:
    """Test TimestampedSchema with timestamp fields."""

    def test_timestamped_schema_has_created_at(self):
        """Test that TimestampedSchema has created_at field."""
        
        class TestSchema(TimestampedSchema):
            name: str
        
        schema = TestSchema(name="test")
        
        assert hasattr(schema, "created_at")
        assert isinstance(schema.created_at, datetime)

    def test_timestamped_schema_created_at_default(self):
        """Test that created_at defaults to current time."""
        
        class TestSchema(TimestampedSchema):
            name: str
        
        before = datetime.utcnow()
        schema = TestSchema(name="test")
        after = datetime.utcnow()
        
        assert before <= schema.created_at <= after

    def test_timestamped_schema_updated_at_optional(self):
        """Test that updated_at is optional."""
        
        class TestSchema(TimestampedSchema):
            name: str
        
        schema = TestSchema(name="test")
        
        assert hasattr(schema, "updated_at")
        assert schema.updated_at is None

    def test_timestamped_schema_updated_at_can_be_set(self):
        """Test that updated_at can be set."""
        
        class TestSchema(TimestampedSchema):
            name: str
        
        now = datetime.utcnow()
        schema = TestSchema(name="test", updated_at=now)
        
        assert schema.updated_at == now

    def test_timestamped_schema_inherits_base_config(self):
        """Test that TimestampedSchema inherits BaseSchema configuration."""
        
        class TestSchema(TimestampedSchema):
            id: UUID
        
        test_uuid = uuid4()
        schema = TestSchema(id=test_uuid)
        
        # Should have from_attributes enabled
        json_data = schema.model_dump_json()
        assert str(test_uuid) in json_data


class TestPaginatedSchema:
    """Test PaginatedSchema with pagination fields."""

    def test_paginated_schema_has_pagination_fields(self):
        """Test that PaginatedSchema has all pagination fields."""
        
        class TestSchema(PaginatedSchema):
            items: List[str]
        
        schema = TestSchema(total=100, page=1, limit=20, pages=5, items=[])
        
        assert schema.total == 100
        assert schema.page == 1
        assert schema.limit == 20
        assert schema.pages == 5

    def test_paginated_schema_has_next_page(self):
        """Test has_next property."""
        
        class TestSchema(PaginatedSchema):
            items: List[str]
        
        # Has next page
        schema1 = TestSchema(total=100, page=1, limit=20, pages=5, items=[])
        assert schema1.has_next is True
        
        # No next page
        schema2 = TestSchema(total=100, page=5, limit=20, pages=5, items=[])
        assert schema2.has_next is False

    def test_paginated_schema_has_previous_page(self):
        """Test has_previous property."""
        
        class TestSchema(PaginatedSchema):
            items: List[str]
        
        # Has previous page
        schema1 = TestSchema(total=100, page=2, limit=20, pages=5, items=[])
        assert schema1.has_previous is True
        
        # No previous page
        schema2 = TestSchema(total=100, page=1, limit=20, pages=5, items=[])
        assert schema2.has_previous is False

    def test_paginated_schema_validation_total(self):
        """Test that total must be >= 0."""
        
        class TestSchema(PaginatedSchema):
            items: List[str]
        
        # Valid
        schema = TestSchema(total=0, page=1, limit=20, pages=0, items=[])
        assert schema.total == 0
        
        # Invalid
        with pytest.raises(ValidationError):
            TestSchema(total=-1, page=1, limit=20, pages=0, items=[])

    def test_paginated_schema_validation_page(self):
        """Test that page must be >= 1."""
        
        class TestSchema(PaginatedSchema):
            items: List[str]
        
        # Valid
        schema = TestSchema(total=100, page=1, limit=20, pages=5, items=[])
        assert schema.page == 1
        
        # Invalid
        with pytest.raises(ValidationError):
            TestSchema(total=100, page=0, limit=20, pages=5, items=[])

    def test_paginated_schema_validation_limit(self):
        """Test that limit must be between 1 and 100."""
        
        class TestSchema(PaginatedSchema):
            items: List[str]
        
        # Valid
        schema = TestSchema(total=100, page=1, limit=50, pages=2, items=[])
        assert schema.limit == 50
        
        # Invalid - too small
        with pytest.raises(ValidationError):
            TestSchema(total=100, page=1, limit=0, pages=5, items=[])
        
        # Invalid - too large
        with pytest.raises(ValidationError):
            TestSchema(total=100, page=1, limit=101, pages=5, items=[])

    def test_paginated_schema_validation_pages(self):
        """Test that pages must be >= 0."""
        
        class TestSchema(PaginatedSchema):
            items: List[str]
        
        # Valid
        schema = TestSchema(total=0, page=1, limit=20, pages=0, items=[])
        assert schema.pages == 0
        
        # Invalid
        with pytest.raises(ValidationError):
            TestSchema(total=100, page=1, limit=20, pages=-1, items=[])

    def test_paginated_schema_inherits_base_config(self):
        """Test that PaginatedSchema inherits BaseSchema configuration."""
        
        class TestSchema(PaginatedSchema):
            items: List[UUID]
        
        test_uuid = uuid4()
        schema = TestSchema(
            total=1,
            page=1,
            limit=20,
            pages=1,
            items=[test_uuid]
        )
        
        # Should have from_attributes enabled
        json_data = schema.model_dump_json()
        assert str(test_uuid) in json_data


class TestCustomValidators:
    """Test custom validators in schemas."""

    def test_custom_validator_in_schema(self):
        """Test that custom validators work in schemas inheriting from BaseSchema."""
        from pydantic import field_validator
        
        class SchemaWithValidator(BaseSchema):
            email: str
            
            @field_validator('email')
            @classmethod
            def validate_email(cls, v):
                if "@" not in v:
                    raise ValueError("Invalid email")
                return v
        
        # Valid email
        schema = SchemaWithValidator(email="test@example.com")
        assert schema.email == "test@example.com"
        
        # Invalid email
        with pytest.raises(ValidationError):
            SchemaWithValidator(email="invalid")

    def test_field_validator_with_constraints(self):
        """Test field validators with constraints."""
        
        class SchemaWithConstraints(BaseSchema):
            age: int = Field(ge=0, le=150)
        
        # Valid
        schema = SchemaWithConstraints(age=25)
        assert schema.age == 25
        
        # Invalid - too small
        with pytest.raises(ValidationError):
            SchemaWithConstraints(age=-1)
        
        # Invalid - too large
        with pytest.raises(ValidationError):
            SchemaWithConstraints(age=151)


class TestSchemaInheritance:
    """Test schema inheritance patterns."""

    def test_nested_schema_inheritance(self):
        """Test nested schema inheritance."""
        
        class AddressSchema(BaseSchema):
            street: str
            city: str
        
        class PersonSchema(BaseSchema):
            name: str
            address: AddressSchema
        
        person = PersonSchema(
            name="John",
            address=AddressSchema(street="123 Main St", city="NYC")
        )
        
        assert person.name == "John"
        assert person.address.street == "123 Main St"

    def test_schema_with_list_of_items(self):
        """Test schema with list of items."""
        
        class ItemSchema(BaseSchema):
            id: UUID
            name: str
        
        class ListSchema(BaseSchema):
            items: List[ItemSchema]
        
        items = [
            ItemSchema(id=uuid4(), name="item1"),
            ItemSchema(id=uuid4(), name="item2"),
        ]
        
        list_schema = ListSchema(items=items)
        assert len(list_schema.items) == 2
        assert list_schema.items[0].name == "item1"


class TestSchemaEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_schema(self):
        """Test empty schema with no fields."""
        
        class EmptySchema(BaseSchema):
            pass
        
        schema = EmptySchema()
        assert schema.model_dump() == {}

    def test_schema_with_many_fields(self):
        """Test schema with many fields."""
        
        class ManyFieldsSchema(BaseSchema):
            field1: str
            field2: int
            field3: float
            field4: bool
            field5: Optional[str] = None
            field6: UUID = Field(default_factory=uuid4)
            field7: datetime = Field(default_factory=datetime.utcnow)
        
        schema = ManyFieldsSchema(
            field1="test",
            field2=42,
            field3=3.14,
            field4=True
        )
        
        assert schema.field1 == "test"
        assert schema.field2 == 42
        assert schema.field3 == 3.14
        assert schema.field4 is True

    def test_schema_with_default_values(self):
        """Test schema with default values."""
        
        class SchemaWithDefaults(BaseSchema):
            name: str
            status: str = "active"
            count: int = 0
        
        schema = SchemaWithDefaults(name="test")
        
        assert schema.name == "test"
        assert schema.status == "active"
        assert schema.count == 0

    def test_schema_model_dump_with_exclude(self):
        """Test model_dump with exclude parameter."""
        
        class TestSchema(BaseSchema):
            name: str
            email: str
            password: str
        
        schema = TestSchema(
            name="john",
            email="john@example.com",
            password="secret"
        )
        
        # Exclude password
        dumped = schema.model_dump(exclude={"password"})
        
        assert "name" in dumped
        assert "email" in dumped
        assert "password" not in dumped

    def test_schema_model_dump_with_include(self):
        """Test model_dump with include parameter."""
        
        class TestSchema(BaseSchema):
            name: str
            email: str
            password: str
        
        schema = TestSchema(
            name="john",
            email="john@example.com",
            password="secret"
        )
        
        # Include only name and email
        dumped = schema.model_dump(include={"name", "email"})
        
        assert "name" in dumped
        assert "email" in dumped
        assert "password" not in dumped


class TestSchemaDocumentation:
    """Test schema documentation and metadata."""

    def test_base_schema_has_docstring(self):
        """Test that BaseSchema has proper docstring."""
        assert BaseSchema.__doc__ is not None
        assert "from_attributes" in BaseSchema.__doc__

    def test_timestamped_schema_has_docstring(self):
        """Test that TimestampedSchema has proper docstring."""
        assert TimestampedSchema.__doc__ is not None
        assert "timestamp" in TimestampedSchema.__doc__

    def test_paginated_schema_has_docstring(self):
        """Test that PaginatedSchema has proper docstring."""
        assert PaginatedSchema.__doc__ is not None
        assert "pagination" in PaginatedSchema.__doc__

    def test_schema_field_descriptions(self):
        """Test that schema fields have descriptions."""
        
        class TestSchema(PaginatedSchema):
            items: List[str]
        
        # Check field info
        assert TestSchema.model_fields["total"].description is not None
        assert TestSchema.model_fields["page"].description is not None
        assert TestSchema.model_fields["limit"].description is not None
