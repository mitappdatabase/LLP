"""
Support ticket system models
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class SupportTicket(Base):
    """Support ticket model"""
    
    __tablename__ = "support_tickets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(String(50), unique=True, nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="SET NULL")
    )
    farmer_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("farmers.id", ondelete="SET NULL"),
        index=True
    )
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    status = Column(String(50), default="open", index=True)  # open, in_progress, waiting, resolved, closed
    assigned_to = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True
    )
    category = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime(timezone=True))
    
    # Relationships
    farmer = relationship("Farmer", back_populates="tickets")
    messages = relationship(
        "TicketMessage", 
        back_populates="ticket",
        cascade="all, delete-orphan",
        order_by="TicketMessage.created_at"
    )
    
    def __repr__(self):
        return f"<SupportTicket {self.ticket_id}>"


class TicketMessage(Base):
    """Ticket message/reply model"""
    
    __tablename__ = "ticket_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("support_tickets.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="SET NULL")
    )
    message = Column(Text, nullable=False)
    attachments = Column(JSONB, default=list)
    is_internal = Column(Boolean, default=False)  # Internal note, not visible to customer
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    ticket = relationship("SupportTicket", back_populates="messages")
    
    def __repr__(self):
        return f"<TicketMessage {self.id}>"
