"""
Pydantic schemas for request/response validation
"""

from .user import (
    UserCreate, UserUpdate, UserResponse, UserLogin, Token, TokenData,
    RoleCreate, RoleResponse, PasswordChange
)
from .product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse,
    ProductImageCreate, ProductImageResponse
)
from .service import ServiceCreate, ServiceUpdate, ServiceResponse
from .project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse,
    ProjectImageCreate, ProjectImageResponse
)
from .blog import (
    BlogCreate, BlogUpdate, BlogResponse, BlogListResponse,
    BlogCategoryCreate, BlogCategoryResponse,
    BlogTagCreate, BlogTagResponse
)
from .career import (
    CareerCreate, CareerUpdate, CareerResponse,
    JobApplicationCreate, JobApplicationResponse
)
from .contact import ContactCreate, ContactResponse, ContactUpdate
from .weather import (
    WeatherStationCreate, WeatherStationResponse,
    WeatherReadingCreate, WeatherReadingResponse
)
from .farmer import FarmerCreate, FarmerResponse, FarmerRegister
from .ticket import (
    SupportTicketCreate, SupportTicketResponse, SupportTicketUpdate,
    TicketMessageCreate, TicketMessageResponse
)
from .training import (
    TrainingEventCreate, TrainingEventResponse,
    TrainingRegistrationCreate, TrainingRegistrationResponse
)
from .tender import GovernmentTenderCreate, GovernmentTenderResponse
from .common import PaginationParams, PaginationResponse, MessageResponse

__all__ = [
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    "RoleCreate",
    "RoleResponse",
    "PasswordChange",
    # Product
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductListResponse",
    "ProductImageCreate",
    "ProductImageResponse",
    # Service
    "ServiceCreate",
    "ServiceUpdate",
    "ServiceResponse",
    # Project
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectListResponse",
    "ProjectImageCreate",
    "ProjectImageResponse",
    # Blog
    "BlogCreate",
    "BlogUpdate",
    "BlogResponse",
    "BlogListResponse",
    "BlogCategoryCreate",
    "BlogCategoryResponse",
    "BlogTagCreate",
    "BlogTagResponse",
    # Career
    "CareerCreate",
    "CareerUpdate",
    "CareerResponse",
    "JobApplicationCreate",
    "JobApplicationResponse",
    # Contact
    "ContactCreate",
    "ContactResponse",
    "ContactUpdate",
    # Weather
    "WeatherStationCreate",
    "WeatherStationResponse",
    "WeatherReadingCreate",
    "WeatherReadingResponse",
    # Farmer
    "FarmerCreate",
    "FarmerResponse",
    "FarmerRegister",
    # Ticket
    "SupportTicketCreate",
    "SupportTicketResponse",
    "SupportTicketUpdate",
    "TicketMessageCreate",
    "TicketMessageResponse",
    # Training
    "TrainingEventCreate",
    "TrainingEventResponse",
    "TrainingRegistrationCreate",
    "TrainingRegistrationResponse",
    # Tender
    "GovernmentTenderCreate",
    "GovernmentTenderResponse",
    # Common
    "PaginationParams",
    "PaginationResponse",
    "MessageResponse",
]
