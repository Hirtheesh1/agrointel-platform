import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy import Uuid as UUID
from app.core.database import Base

class BaseModel(Base):
    """
    Abstract Base Model that provides universally required fields:
    - id (UUID)
    - created_at
    - updated_at
    """
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
