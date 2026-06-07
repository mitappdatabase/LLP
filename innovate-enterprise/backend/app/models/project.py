"""
Project portfolio models
"""

from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Text, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class Project(Base):
    """Project model for portfolio management"""
    
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    client = Column(String(255), index=True)
    location = Column(String(255), index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    value = Column(Numeric(15, 2))
    technologies = Column(JSONB, default=list)
    description = Column(Text, nullable=False)
    outcomes = Column(Text)
    case_study_url = Column(String(500))
    seo_metadata_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("seo_metadata.id", ondelete="CASCADE")
    )
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = relationship(
        "ProjectImage", 
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="ProjectImage.display_order"
    )
    seo_metadata = relationship("SEOMetadata", uselist=False)
    
    def __repr__(self):
        return f"<Project {self.title}>"


class ProjectImage(Base):
    """Project image model"""
    
    __tablename__ = "project_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("projects.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    image_url = Column(String(500), nullable=False)
    display_order = Column(Integer, default=0)
    caption = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="images")
    
    def __repr__(self):
        return f"<ProjectImage {self.id}>"
