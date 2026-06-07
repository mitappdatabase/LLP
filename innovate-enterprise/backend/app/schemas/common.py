"""
Common schemas used across the application
"""

from datetime import datetime
from typing import Optional, List, Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints"""
    
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$", description="Sort order")
    search: Optional[str] = Field(default=None, description="Search query")


class PaginationResponse(BaseModel, Generic[T]):
    """Paginated response wrapper"""
    
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Simple message response"""
    
    message: str
    detail: Optional[str] = None


class TimestampMixin(BaseModel):
    """Mixin for created_at and updated_at timestamps"""
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
