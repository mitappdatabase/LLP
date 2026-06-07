"""
User schemas for authentication and user management
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator
import uuid


# Role Schemas
class RoleCreate(BaseModel):
    """Schema for creating a role"""
    
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    permissions: List[str] = []


class RoleResponse(BaseModel):
    """Schema for role response"""
    
    id: uuid.UUID
    name: str
    description: Optional[str]
    permissions: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a user"""
    
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    role_id: Optional[uuid.UUID] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    role_id: Optional[uuid.UUID] = None


class UserResponse(UserBase):
    """Schema for user response"""
    
    id: uuid.UUID
    role_id: Optional[uuid.UUID]
    role: Optional[RoleResponse] = None
    is_superuser: bool
    full_name: str
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Schema for decoded token data"""
    
    sub: Optional[str] = None
    exp: Optional[datetime] = None
    type: Optional[str] = None


class PasswordChange(BaseModel):
    """Schema for password change"""
    
    current_password: str
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v
