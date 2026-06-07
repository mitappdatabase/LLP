"""
Blog CMS models
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Integer, Text, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


# Association table for blog posts and tags (many-to-many)
blog_post_tags = Table(
    "blog_post_tags",
    Base.metadata,
    Column("blog_id", UUID(as_uuid=True), ForeignKey("blogs.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("blog_tags.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime(timezone=True), default=datetime.utcnow),
)


class BlogCategory(Base):
    """Blog category model"""
    
    __tablename__ = "blog_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    parent_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("blog_categories.id", ondelete="CASCADE")
    )
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    children = relationship("BlogCategory", backref="parent", remote_side=[id])
    blogs = relationship("Blog", back_populates="category")
    
    def __repr__(self):
        return f"<BlogCategory {self.name}>"


class BlogTag(Base):
    """Blog tag model"""
    
    __tablename__ = "blog_tags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    blogs = relationship("Blog", secondary=blog_post_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<BlogTag {self.name}>"


class Blog(Base):
    """Blog post model"""
    
    __tablename__ = "blogs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    excerpt = Column(Text)
    author_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True
    )
    category_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("blog_categories.id", ondelete="SET NULL"),
        index=True
    )
    featured_image = Column(String(500))
    is_published = Column(Boolean, default=False, index=True)
    view_count = Column(Integer, default=0)
    seo_metadata_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("seo_metadata.id", ondelete="CASCADE")
    )
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = relationship("User", back_populates="blogs")
    category = relationship("BlogCategory", back_populates="blogs")
    tags = relationship("BlogTag", secondary=blog_post_tags, back_populates="blogs")
    seo_metadata = relationship("SEOMetadata", uselist=False)
    
    def __repr__(self):
        return f"<Blog {self.title}>"
