"""
Career and job application models
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Integer, Text, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class Career(Base):
    """Career/Job opening model"""
    
    __tablename__ = "careers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    department = Column(String(100))
    location = Column(String(100))
    employment_type = Column(String(50))  # full-time, part-time, contract, internship
    description = Column(Text, nullable=False)
    requirements = Column(JSONB, default=list)
    responsibilities = Column(JSONB, default=list)
    experience_level = Column(String(50))
    salary_min = Column(Numeric(10, 2))
    salary_max = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = relationship(
        "JobApplication", 
        back_populates="career",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Career {self.title}>"


class JobApplication(Base):
    """Job application model"""
    
    __tablename__ = "job_applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    career_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("careers.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    mobile = Column(String(20))
    qualification = Column(String(255))
    experience_years = Column(Integer, default=0)
    resume_url = Column(String(500), nullable=False)
    cover_letter = Column(Text)
    status = Column(String(50), default="pending", index=True)  # pending, reviewed, shortlisted, rejected, hired
    applied_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    career = relationship("Career", back_populates="applications")
    
    def __repr__(self):
        return f"<JobApplication {self.full_name} - {self.career_id}>"
