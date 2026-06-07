"""
Training and workshop registration models
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Integer, Numeric, Text, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class TrainingEvent(Base):
    """Training event/workshop model"""
    
    __tablename__ = "training_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    location = Column(String(255))
    venue_details = Column(Text)
    max_participants = Column(Integer, default=50)
    registered_count = Column(Integer, default=0)
    fee = Column(Numeric(10, 2), default=0)
    currency = Column(String(10), default="INR")
    trainer_name = Column(String(255))
    trainer_bio = Column(Text)
    agenda = Column(JSONB, default=list)
    prerequisites = Column(Text)
    certificate_provided = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    registrations = relationship(
        "TrainingRegistration", 
        back_populates="event",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<TrainingEvent {self.title}>"


class TrainingRegistration(Base):
    """Training registration model"""
    
    __tablename__ = "training_registrations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("training_events.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(20), nullable=False)
    organization = Column(String(255))
    designation = Column(String(100))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    payment_status = Column(String(50), default="pending")  # pending, paid, refunded, waived
    payment_method = Column(String(50))
    transaction_id = Column(String(100))
    attendance_status = Column(String(50), default="registered")  # registered, attended, absent, cancelled
    feedback_rating = Column(Integer)  # 1-5
    feedback_comments = Column(Text)
    certificate_issued = Column(Boolean, default=False)
    registered_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    event = relationship("TrainingEvent", back_populates="registrations")
    
    def __repr__(self):
        return f"<TrainingRegistration {self.full_name} - {self.event_id}>"
