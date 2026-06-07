"""
User, Role, and Permission models
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class Role(Base):
    """User role model for RBAC"""
    
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)
    permissions = Column(JSONB, default=list)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="role")
    
    def __repr__(self):
        return f"<Role {self.name}>"


class Permission(Base):
    """Permission model for fine-grained access control"""
    
    __tablename__ = "permissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    resource = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Permission {self.name}>"


class User(Base):
    """User model for authentication and authorization"""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="SET NULL"), index=True)
    is_active = Column(Boolean, default=True, index=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    role = relationship("Role", back_populates="users")
    blogs = relationship("Blog", back_populates="author")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    @property
    def is_superuser(self) -> bool:
        """Check if user has super_admin role"""
        return self.role and self.role.name == "super_admin"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    def __repr__(self):
        return f"<User {self.email}>"
