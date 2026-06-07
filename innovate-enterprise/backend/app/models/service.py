"""
Service model for services catalogue
"""

from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class Service(Base):
    """Service model for services management"""
    
    __tablename__ = "services"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    features = Column(JSONB, default=list)
    icon = Column(String(100))
    seo_metadata_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("seo_metadata.id", ondelete="CASCADE")
    )
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    seo_metadata = relationship("SEOMetadata", uselist=False)
    
    def __repr__(self):
        return f"<Service {self.name}>"
