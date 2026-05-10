from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class ORMBaseSchema(BaseModel):
    """
    Base schema for all schemas that will interact with SQLAlchemy ORM models.
    Sets from_attributes=True for compatibility with SQLAlchemy.
    """
    model_config = ConfigDict(from_attributes=True)

class IDModelMixin(BaseModel):
    """
    Mixin for adding UUID 'id' to response schemas.
    """
    id: UUID

class TimestampMixin(BaseModel):
    """
    Mixin for adding created_at and updated_at to response schemas.
    """
    created_at: datetime
    updated_at: datetime
