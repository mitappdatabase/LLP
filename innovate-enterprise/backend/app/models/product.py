"""
Product model for product catalogue
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class Product(Base):
    """Product model for product catalogue management"""
    
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    specifications = Column(JSONB, default=dict)
    features = Column(JSONB, default=list)
    applications = Column(JSONB, default=list)
    status = Column(String(20), default="active", index=True)
    seo_metadata_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("seo_metadata.id", ondelete="CASCADE")
    )
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = relationship(
        "ProductImage", 
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="ProductImage.display_order"
    )
    seo_metadata = relationship("SEOMetadata", uselist=False)
    
    def __repr__(self):
        return f"<Product {self.name}>"


class ProductImage(Base):
    """Product image model"""
    
    __tablename__ = "product_images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("products.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    image_url = Column(String(500), nullable=False)
    display_order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="images")
    
    def __repr__(self):
        return f"<ProductImage {self.id}>"
