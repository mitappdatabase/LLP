"""
Pydantic Schemas for Request/Response Validation
All API data validation and serialization models
"""

from pydantic import BaseModel, EmailStr, Field, validator, constr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ==================== SHARED SCHEMAS ====================

class PaginationParams(BaseModel):
    """Common pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field(None, description="Field to sort by")
    sort_order: str = Field("desc", pattern="^(asc|desc)$", description="Sort order")


class PaginationResponse(BaseModel):
    """Common pagination response metadata"""
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class ResponseBase(BaseModel):
    """Base response schema"""
    success: bool = True
    message: Optional[str] = None


# ==================== AUTH SCHEMAS ====================

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: constr(min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: constr(min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user"""
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=3, max_length=100)] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    role: str
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """JWT token payload"""
    sub: str  # user ID
    exp: datetime
    type: str  # access or refresh


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """Change password request"""
    current_password: str
    new_password: constr(min_length=8)


# ==================== PRODUCT SCHEMAS ====================

class ProductCategoryEnum(str, Enum):
    WEATHER_STATIONS = "weather_stations"
    IOT_DEVICES = "iot_devices"
    AGRICULTURAL_SOLUTIONS = "agricultural_solutions"
    RENEWABLE_ENERGY = "renewable_energy"
    ELECTRONICS_SYSTEMS = "electronics_systems"
    SOFTWARE_SOLUTIONS = "software_solutions"


class ProductBase(BaseModel):
    """Base product schema"""
    name: str
    category: ProductCategoryEnum
    short_description: Optional[str] = None
    detailed_description: Optional[str] = None
    price: Optional[float] = None
    status: bool = True


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    product_id: str
    technical_specifications: Optional[Dict[str, Any]] = None
    features: Optional[List[str]] = None
    applications: Optional[List[str]] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    slug: str


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = None
    category: Optional[ProductCategoryEnum] = None
    short_description: Optional[str] = None
    detailed_description: Optional[str] = None
    technical_specifications: Optional[Dict[str, Any]] = None
    features: Optional[List[str]] = None
    applications: Optional[List[str]] = None
    price: Optional[float] = None
    status: Optional[bool] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class ProductImageBase(BaseModel):
    """Base product image schema"""
    image_url: str
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    order: int = 0
    is_primary: bool = False


class ProductImageResponse(ProductImageBase):
    """Product image response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductDatasheetBase(BaseModel):
    """Base product datasheet schema"""
    file_url: str
    file_name: str
    language: str = "en"
    version: Optional[str] = None


class ProductDatasheetResponse(ProductDatasheetBase):
    """Product datasheet response"""
    id: int
    file_size: Optional[int] = None
    uploaded_at: datetime
    
    class Config:
        from_attributes = True


class ProductResponse(ProductBase):
    """Product response schema"""
    id: int
    product_id: str
    slug: str
    currency: str
    stock_status: str
    meta_keywords: Optional[str] = None
    translations: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    images: List[ProductImageResponse] = []
    datasheets: List[ProductDatasheetResponse] = []
    
    class Config:
        from_attributes = True


class ProductListResponse(ResponseBase):
    """Product list response with pagination"""
    data: List[ProductResponse]
    pagination: PaginationResponse


# ==================== SERVICE SCHEMAS ====================

class ServiceCategoryEnum(str, Enum):
    CONSULTANCY = "consultancy"
    TRAINING = "training"
    AI_SOLUTIONS = "ai_solutions"
    IOT_DEVELOPMENT = "iot_development"
    WEATHER_MONITORING = "weather_monitoring"
    RENEWABLE_ENERGY = "renewable_energy"
    SURVEY_DATA = "survey_data"
    GOVERNMENT_PROJECTS = "government_projects"


class ServiceBase(BaseModel):
    """Base service schema"""
    name: str
    category: ServiceCategoryEnum
    short_description: Optional[str] = None
    detailed_description: Optional[str] = None
    status: bool = True


class ServiceCreate(ServiceBase):
    """Schema for creating a service"""
    features: Optional[List[str]] = None
    deliverables: Optional[List[str]] = None
    pricing_model: Optional[str] = None
    duration: Optional[str] = None
    slug: str


class ServiceUpdate(BaseModel):
    """Schema for updating a service"""
    name: Optional[str] = None
    category: Optional[ServiceCategoryEnum] = None
    short_description: Optional[str] = None
    detailed_description: Optional[str] = None
    features: Optional[List[str]] = None
    deliverables: Optional[List[str]] = None
    status: Optional[bool] = None


class ServiceResponse(ServiceBase):
    """Service response schema"""
    id: int
    slug: str
    translations: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== PROJECT SCHEMAS ====================

class ProjectStatusEnum(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class ProjectBase(BaseModel):
    """Base project schema"""
    title: str
    client_name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: ProjectStatusEnum = ProjectStatusEnum.COMPLETED


class ProjectCreate(ProjectBase):
    """Schema for creating a project"""
    client_type: Optional[str] = None
    state: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    project_value: Optional[float] = None
    objectives: Optional[List[str]] = None
    outcomes: Optional[List[str]] = None
    technologies: Optional[List[str]] = None
    is_featured: bool = False
    slug: str


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    title: Optional[str] = None
    client_name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatusEnum] = None
    is_featured: Optional[bool] = None


class ProjectResponse(ProjectBase):
    """Project response schema"""
    id: int
    slug: str
    client_type: Optional[str] = None
    state: Optional[str] = None
    country: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    duration_months: Optional[int] = None
    project_value: Optional[float] = None
    currency: str
    objectives: Optional[List[str]] = None
    outcomes: Optional[List[str]] = None
    is_featured: bool
    case_study_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== BLOG SCHEMAS ====================

class BlogStatusEnum(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class BlogBase(BaseModel):
    """Base blog schema"""
    title: str
    excerpt: Optional[str] = None
    content: str
    author_name: Optional[str] = None


class BlogCreate(BlogBase):
    """Schema for creating a blog"""
    slug: str
    category_id: Optional[int] = None
    featured_image: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    tags: Optional[List[str]] = None
    status: BlogStatusEnum = BlogStatusEnum.DRAFT


class BlogUpdate(BaseModel):
    """Schema for updating a blog"""
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    featured_image: Optional[str] = None
    status: Optional[BlogStatusEnum] = None
    is_featured: Optional[bool] = None


class BlogCategoryBase(BaseModel):
    """Base blog category schema"""
    name: str
    slug: str


class BlogCategoryResponse(BlogCategoryBase):
    """Blog category response"""
    id: int
    description: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class BlogTagBase(BaseModel):
    """Base blog tag schema"""
    name: str
    slug: str


class BlogTagResponse(BlogTagBase):
    """Blog tag response"""
    id: int
    
    class Config:
        from_attributes = True


class BlogResponse(BlogBase):
    """Blog response schema"""
    id: int
    slug: str
    featured_image: Optional[str] = None
    featured_image_alt: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    status: BlogStatusEnum
    is_featured: bool
    views_count: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[BlogCategoryResponse] = None
    tags: List[BlogTagResponse] = []
    
    class Config:
        from_attributes = True


# ==================== CAREER SCHEMAS ====================

class JobTypeEnum(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class CareerBase(BaseModel):
    """Base career schema"""
    title: str
    department: Optional[str] = None
    location: str
    job_type: JobTypeEnum
    description: Optional[str] = None


class CareerCreate(CareerBase):
    """Schema for creating a career"""
    requirements: Optional[List[str]] = None
    responsibilities: Optional[List[str]] = None
    experience_min: Optional[int] = None
    experience_max: Optional[int] = None
    is_active: bool = True
    slug: str


class CareerUpdate(BaseModel):
    """Schema for updating a career"""
    title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[JobTypeEnum] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CareerResponse(CareerBase):
    """Career response schema"""
    id: int
    slug: str
    experience_min: Optional[int] = None
    experience_max: Optional[int] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    is_active: bool
    application_deadline: Optional[datetime] = None
    openings_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ApplicationStatusEnum(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    HIRED = "hired"


class JobApplicationBase(BaseModel):
    """Base job application schema"""
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    highest_qualification: str
    total_experience: Optional[float] = None


class JobApplicationCreate(JobApplicationBase):
    """Schema for creating a job application"""
    career_id: int
    institution: Optional[str] = None
    graduation_year: Optional[int] = None
    current_company: Optional[str] = None
    current_designation: Optional[str] = None
    cover_letter: Optional[str] = None
    resume_url: str
    resume_file_name: str


class JobApplicationResponse(JobApplicationBase):
    """Job application response"""
    id: int
    career_id: int
    status: ApplicationStatusEnum
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== CONTACT SCHEMAS ====================

class ContactStatusEnum(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ContactBase(BaseModel):
    """Base contact schema"""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str


class ContactCreate(ContactBase):
    """Schema for creating a contact inquiry"""
    company: Optional[str] = None
    inquiry_type: Optional[str] = None
    interested_in: Optional[List[str]] = None


class ContactUpdate(BaseModel):
    """Schema for updating a contact"""
    status: Optional[ContactStatusEnum] = None
    response: Optional[str] = None
    assigned_to: Optional[int] = None


class ContactResponse(ContactBase):
    """Contact response schema"""
    id: int
    company: Optional[str] = None
    inquiry_type: Optional[str] = None
    status: ContactStatusEnum
    ip_address: Optional[str] = None
    is_spam: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== FARMER SCHEMAS ====================

class FarmerBase(BaseModel):
    """Base farmer schema"""
    first_name: str
    last_name: str
    phone: str
    email: Optional[EmailStr] = None
    village: str
    district: str
    state: str
    pincode: str


class FarmerCreate(FarmerBase):
    """Schema for registering a farmer"""
    father_husband_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    alternate_phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    taluka: Optional[str] = None
    total_land_area: Optional[float] = None
    soil_type: Optional[str] = None
    primary_crops: Optional[List[str]] = None
    farmer_type: Optional[str] = None
    is_fpo_member: bool = False
    preferred_language: str = "mr"


class FarmerUpdate(BaseModel):
    """Schema for updating farmer"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_verified: Optional[bool] = None


class FarmerResponse(FarmerBase):
    """Farmer response schema"""
    id: int
    registration_number: str
    father_husband_name: Optional[str] = None
    taluka: Optional[str] = None
    total_land_area: Optional[float] = None
    soil_type: Optional[str] = None
    primary_crops: Optional[List[str]] = None
    farmer_type: Optional[str] = None
    is_fpo_member: bool
    is_verified: bool
    preferred_language: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== WEATHER STATION SCHEMAS ====================

class WeatherReadingBase(BaseModel):
    """Base weather reading schema"""
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    rainfall: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[int] = None
    solar_radiation: Optional[float] = None
    soil_temperature: Optional[float] = None
    soil_moisture: Optional[float] = None


class WeatherReadingCreate(WeatherReadingBase):
    """Schema for creating weather reading"""
    station_id: int
    reading_timestamp: datetime


class WeatherReadingResponse(WeatherReadingBase):
    """Weather reading response"""
    id: int
    station_id: int
    quality_flag: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class WeatherStationBase(BaseModel):
    """Base weather station schema"""
    station_id: str
    location_name: str
    latitude: float
    longitude: float
    model: Optional[str] = None


class WeatherStationResponse(WeatherStationBase):
    """Weather station response"""
    id: int
    farmer_id: Optional[int] = None
    installation_date: Optional[datetime] = None
    status: str
    last_data_received: Optional[datetime] = None
    battery_level: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== TRAINING SCHEMAS ====================

class TrainingBase(BaseModel):
    """Base training schema"""
    title: str
    description: Optional[str] = None
    category: str
    start_date: datetime
    end_date: Optional[datetime] = None
    venue: Optional[str] = None
    city: str
    state: str
    is_online: bool = False


class TrainingCreate(TrainingBase):
    """Schema for creating training"""
    total_seats: int = 30
    fee_amount: float = 0
    trainer_name: Optional[str] = None
    registration_deadline: Optional[datetime] = None


class TrainingResponse(TrainingBase):
    """Training response schema"""
    id: int
    slug: str
    total_seats: int
    registered_count: int
    fee_amount: float
    status: str
    banner_image: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== TENDER SCHEMAS ====================

class TenderStatusEnum(str, Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    CLOSED = "closed"
    AWARDED = "awarded"


class TenderBase(BaseModel):
    """Base tender schema"""
    tender_number: str
    title: str
    organization_name: str
    publish_date: datetime
    bid_submission_deadline: datetime
    status: TenderStatusEnum = TenderStatusEnum.UPCOMING


class TenderResponse(TenderBase):
    """Tender response schema"""
    id: int
    description: Optional[str] = None
    estimated_value: Optional[float] = None
    location: Optional[str] = None
    state: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ==================== SUPPORT TICKET SCHEMAS ====================

class TicketPriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketStatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class SupportTicketBase(BaseModel):
    """Base support ticket schema"""
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    subject: str
    description: str
    priority: TicketPriorityEnum = TicketPriorityEnum.MEDIUM


class SupportTicketCreate(SupportTicketBase):
    """Schema for creating support ticket"""
    product_id: Optional[int] = None
    category: Optional[str] = None


class SupportTicketResponse(SupportTicketBase):
    """Support ticket response"""
    id: int
    ticket_number: str
    status: TicketStatusEnum
    category: Optional[str] = None
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TicketMessageBase(BaseModel):
    """Base ticket message schema"""
    message: str
    is_internal: bool = False


class TicketMessageCreate(TicketMessageBase):
    """Schema for creating ticket message"""
    ticket_id: int


class TicketMessageResponse(TicketMessageBase):
    """Ticket message response"""
    id: int
    ticket_id: int
    sender_type: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== DASHBOARD SCHEMAS ====================

class DashboardMetrics(BaseModel):
    """Dashboard metrics response"""
    total_visitors: int
    total_leads: int
    total_products: int
    total_projects: int
    total_blogs: int
    total_contacts: int
    total_farmers: int
    pending_tickets: int
    recent_applications: int
    
    # Charts data
    visitor_trend: List[Dict[str, Any]] = []
    lead_trend: List[Dict[str, Any]] = []


# ==================== DOWNLOAD SCHEMAS ====================

class DownloadBase(BaseModel):
    """Base download schema"""
    title: str
    description: Optional[str] = None
    file_url: str
    file_name: str
    category: str
    is_public: bool = True


class DownloadResponse(DownloadBase):
    """Download response"""
    id: int
    file_type: str
    file_size: Optional[int] = None
    download_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== MEDIA GALLERY SCHEMAS ====================

class MediaGalleryBase(BaseModel):
    """Base media gallery schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    media_type: str
    file_url: str
    category: str
    is_public: bool = True


class MediaGalleryResponse(MediaGalleryBase):
    """Media gallery response"""
    id: int
    thumbnail_url: Optional[str] = None
    file_size: Optional[int] = None
    views_count: int
    tags: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== TESTIMONIAL SCHEMAS ====================

class TestimonialBase(BaseModel):
    """Base testimonial schema"""
    client_name: str
    client_designation: Optional[str] = None
    client_organization: Optional[str] = None
    testimonial_text: str
    rating: int = 5


class TestimonialResponse(TestimonialBase):
    """Testimonial response"""
    id: int
    client_location: Optional[str] = None
    client_photo_url: Optional[str] = None
    is_verified: bool
    is_featured: bool
    display_order: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== PARTNER SCHEMAS ====================

class PartnerBase(BaseModel):
    """Base partner schema"""
    name: str
    partner_type: str
    logo_url: Optional[str] = None
    website_url: Optional[str] = None


class PartnerResponse(PartnerBase):
    """Partner response"""
    id: int
    industry: Optional[str] = None
    location: Optional[str] = None
    is_featured: bool
    display_order: int
    status: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== ERROR RESPONSE ====================

class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: str
    detail: Optional[Any] = None
    status_code: int
