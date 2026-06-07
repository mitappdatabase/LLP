"""
Farmer registration portal models
"""

from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class Farmer(Base):
    """Farmer registration model"""
    
    __tablename__ = "farmers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255))
    mobile = Column(String(20), nullable=False, index=True)
    address = Column(Text)
    village = Column(String(255))
    district = Column(String(100), index=True)
    state = Column(String(100), index=True)
    pincode = Column(String(10))
    land_area = Column(Numeric(10, 2))
    land_unit = Column(String(20), default="acres")
    primary_crop = Column(String(100))
    crops_grown = Column(JSONB, default=list)
    aadhaar_number = Column(String(12))
    is_verified = Column(Boolean, default=False)
    is_registered = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tickets = relationship("SupportTicket", back_populates="farmer")
    
    def __repr__(self):
        return f"<Farmer {self.full_name}>"
