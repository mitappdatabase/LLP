"""
Government tender/project showcase models
"""

from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class GovernmentTender(Base):
    """Government tender/project model"""
    
    __tablename__ = "government_tenders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    ministry = Column(String(255))
    description = Column(Text, nullable=False)
    scope_of_work = Column(Text)
    budget = Column(Numeric(15, 2))
    currency = Column(String(10), default="INR")
    publish_date = Column(Date, nullable=False)
    deadline = Column(Date, nullable=False, index=True)
    status = Column(String(50), default="open", index=True)  # open, closed, awarded, cancelled, expired
    award_value = Column(Numeric(15, 2))
    award_date = Column(Date)
    document_url = Column(String(500))
    eligibility_criteria = Column(JSONB, default=list)
    submission_link = Column(String(500))
    contact_person = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<GovernmentTender {self.title}>"
