import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from db.db import Base


class ShortUrl(Base):
    """Модель сокращенного url."""
    __tablename__ = "short_url"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(URLType, nullable=False)
    url_id = Column(String(8), index=True, nullable=False)
    short_url = Column(URLType, nullable=False)
    usages_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    url_history = relationship('ShortUrlHistory', cascade="all, delete")


class ShortUrlHistory(Base):
    """История использования"""
    __tablename__ = "short_url_history"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    short_url = Column(
        UUID(as_uuid=True),
        ForeignKey('short_url.id', ondelete="CASCADE"),
        nullable=False,
    )
    client = Column(String(50), nullable=False)
    use_at = Column(DateTime, index=True, default=datetime.utcnow)
