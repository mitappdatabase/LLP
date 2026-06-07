"""
SEO metadata model for all content types
"""

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

from app.db.session import Base


class SEOMetadata(Base):
    """SEO metadata model for optimizing pages"""
    
    __tablename__ = "seo_metadata"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meta_title = Column(String(255))
    meta_description = Column(Text)
    meta_keywords = Column(Text)
    og_title = Column(String(255))
    og_description = Column(Text)
    og_image = Column(String(500))
    canonical_url = Column(String(500))
    structured_data = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SEOMetadata {self.meta_title}>"
