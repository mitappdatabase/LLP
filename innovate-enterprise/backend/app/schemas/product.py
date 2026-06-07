"""
Product schemas for product catalogue management
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid


class ProductImageCreate(BaseModel):
    """Schema for creating a product image"""
    
    image_url: str = Field(..., max_length=500)
    display_order: int = Field(default=0, ge=0)
    is_primary: bool = False


class ProductImageResponse(BaseModel):
    """Schema for product image response"""
    
    id: uuid.UUID
    product_id: uuid.UUID
    image_url: str
    display_order: int
    is_primary: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """Base product schema"""
    
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    description: str
    specifications: Optional[Dict[str, Any]] = {}
    features: Optional[List[str]] = []
    applications: Optional[List[str]] = []
    status: str = Field(default="active", pattern="^(active|inactive|discontinued)$")


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    
    product_id: str = Field(..., min_length=1, max_length=50)
    images: Optional[List[ProductImageCreate]] = []


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = None
    features: Optional[List[str]] = None
    applications: Optional[List[str]] = None
    status: Optional[str] = Field(None, pattern="^(active|inactive|discontinued)$")


class ProductResponse(ProductBase):
    """Schema for product response"""
    
    id: uuid.UUID
    product_id: str
    images: Optional[List[ProductImageResponse]] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for product list with pagination"""
    
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    class Config:
        from_attributes = True
