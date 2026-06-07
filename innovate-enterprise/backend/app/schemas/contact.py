"""
Contact schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
import uuid


class ContactBase(BaseModel):
    """Base contact schema"""
    
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)


class ContactCreate(ContactBase):
    """Schema for creating a contact inquiry"""
    
    company: Optional[str] = Field(None, max_length=255)
    mobile: Optional[str] = Field(None, max_length=20)


class ContactUpdate(BaseModel):
    """Schema for updating a contact inquiry"""
    
    status: Optional[str] = Field(None, pattern="^(new|contacted|resolved|closed)$")
    notes: Optional[str] = None
    assigned_to: Optional[uuid.UUID] = None


class ContactResponse(ContactBase):
    """Schema for contact response"""
    
    id: uuid.UUID
    company: Optional[str]
    mobile: Optional[str]
    status: str
    source: str
    assigned_to: Optional[uuid.UUID]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
