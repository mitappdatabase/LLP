"""
SQLAlchemy models for database tables
"""

from .user import User, Role, Permission
from .product import Product, ProductImage
from .service import Service
from .project import Project, ProjectImage
from .blog import Blog, BlogCategory, BlogTag, blog_post_tags
from .career import Career, JobApplication
from .contact import Contact
from .weather import WeatherStation, WeatherReading
from .farmer import Farmer
from .ticket import SupportTicket, TicketMessage
from .training import TrainingEvent, TrainingRegistration
from .tender import GovernmentTender
from .seo import SEOMetadata
from .audit import AuditLog

__all__ = [
    "User",
    "Role",
    "Permission",
    "Product",
    "ProductImage",
    "Service",
    "Project",
    "ProjectImage",
    "Blog",
    "BlogCategory",
    "BlogTag",
    "blog_post_tags",
    "Career",
    "JobApplication",
    "Contact",
    "WeatherStation",
    "WeatherReading",
    "Farmer",
    "SupportTicket",
    "TicketMessage",
    "TrainingEvent",
    "TrainingRegistration",
    "GovernmentTender",
    "SEOMetadata",
    "AuditLog",
]
