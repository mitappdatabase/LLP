"""
Database Models for Innovate Enterprise LLP
Comprehensive schema for all business modules
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, Table, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.db.session import Base


# ==================== ENUMS ====================

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MANAGER = "manager"
    EDITOR = "editor"
    VIEWER = "viewer"


class ProductCategory(str, enum.Enum):
    WEATHER_STATIONS = "weather_stations"
    IOT_DEVICES = "iot_devices"
    AGRICULTURAL_SOLUTIONS = "agricultural_solutions"
    RENEWABLE_ENERGY = "renewable_energy"
    ELECTRONICS_SYSTEMS = "electronics_systems"
    SOFTWARE_SOLUTIONS = "software_solutions"


class ServiceCategory(str, enum.Enum):
    CONSULTANCY = "consultancy"
    TRAINING = "training"
    AI_SOLUTIONS = "ai_solutions"
    IOT_DEVELOPMENT = "iot_development"
    WEATHER_MONITORING = "weather_monitoring"
    RENEWABLE_ENERGY = "renewable_energy"
    SURVEY_DATA = "survey_data"
    GOVERNMENT_PROJECTS = "government_projects"


class ProjectStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class BlogStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class JobType(str, enum.Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"


class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    HIRED = "hired"


class ContactStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TenderStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    CLOSED = "closed"
    AWARDED = "awarded"


# ==================== ASSOCIATION TABLES ====================

blog_tags_assoc = Table(
    'blog_tags_assoc',
    Base.metadata,
    Column('blog_id', Integer, ForeignKey('blogs.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('blog_tags.id'), primary_key=True)
)

project_technologies_assoc = Table(
    'project_technologies_assoc',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('technology_id', Integer, ForeignKey('technologies.id'), primary_key=True)
)


# ==================== USER & AUTH MODELS ====================

class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(Base):
    """Refresh token model for JWT authentication"""
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(String(500))

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")


# ==================== ROLE & PERMISSION MODELS ====================

class Role(Base):
    """Role model for RBAC"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")


class Permission(Base):
    """Permission model for RBAC"""
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    resource = Column(String(100), nullable=False)  # e.g., 'products', 'blogs'
    action = Column(String(50), nullable=False)  # e.g., 'create', 'read', 'update', 'delete'
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")


role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
)


# ==================== PRODUCT MODELS ====================

class Product(Base):
    """Product model for product catalogue"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(50), unique=True, index=True, nullable=False)  # Custom product ID
    name = Column(String(255), nullable=False)
    category = Column(SQLEnum(ProductCategory), nullable=False)
    short_description = Column(String(500))
    detailed_description = Column(Text)
    technical_specifications = Column(JSON)  # Flexible specs storage
    features = Column(JSON)  # List of features
    applications = Column(JSON)  # List of applications
    status = Column(Boolean, default=True)  # Active/Inactive
    price = Column(Float)
    currency = Column(String(3), default="INR")
    stock_status = Column(String(50), default="available")  # available, out_of_stock, made_to_order
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    meta_keywords = Column(String(500))
    slug = Column(String(255), unique=True, index=True)
    
    # Multi-language support
    translations = Column(JSON)  # {mr: {name, description, etc.}}
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.id'))

    # Relationships
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan", order_by="ProductImage.order")
    datasheets = relationship("ProductDatasheet", back_populates="product", cascade="all, delete-orphan")


class ProductImage(Base):
    """Product images"""
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    caption = Column(String(500))
    order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="images")


class ProductDatasheet(Base):
    """Product datasheet PDFs"""
    __tablename__ = "product_datasheets"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer)  # in bytes
    language = Column(String(2), default="en")
    version = Column(String(20))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="datasheets")


# ==================== SERVICE MODELS ====================

class Service(Base):
    """Service model for service offerings"""
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(SQLEnum(ServiceCategory), nullable=False)
    short_description = Column(String(500))
    detailed_description = Column(Text)
    features = Column(JSON)
    deliverables = Column(JSON)
    pricing_model = Column(String(100))  # fixed, hourly, project_based
    duration = Column(String(100))  # estimated duration
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    slug = Column(String(255), unique=True, index=True)
    
    # Multi-language
    translations = Column(JSON)
    
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    images = relationship("ServiceImage", back_populates="service", cascade="all, delete-orphan")


class ServiceImage(Base):
    """Service images"""
    __tablename__ = "service_images"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    service = relationship("Service", back_populates="images")


# ==================== PROJECT MODELS ====================

class Project(Base):
    """Project portfolio model"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    client_name = Column(String(255))
    client_type = Column(String(100))  # farmer, fpo, university, government, etc.
    location = Column(String(255))
    state = Column(String(100))
    country = Column(String(100), default="India")
    
    # Timeline
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    duration_months = Column(Integer)
    
    # Financials
    project_value = Column(Float)
    currency = Column(String(3), default="INR")
    
    # Content
    description = Column(Text)
    objectives = Column(JSON)
    outcomes = Column(JSON)
    challenges = Column(Text)
    solutions = Column(Text)
    
    # Status
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.COMPLETED)
    is_featured = Column(Boolean, default=False)
    
    # Case Study
    case_study_url = Column(String(500))
    case_study_file_size = Column(Integer)
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    slug = Column(String(255), unique=True, index=True)
    
    # Multi-language
    translations = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    images = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan", order_by="ProjectImage.order")
    technologies = relationship("Technology", secondary=project_technologies_assoc, back_populates="projects")


class ProjectImage(Base):
    """Project images"""
    __tablename__ = "project_images"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    caption = Column(String(500))
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="images")


class Technology(Base):
    """Technologies used in projects"""
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(100))  # hardware, software, ai, iot, etc.
    logo_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    projects = relationship("Project", secondary=project_technologies_assoc, back_populates="technologies")


# ==================== BLOG MODELS ====================

class Blog(Base):
    """Blog/Article model"""
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    excerpt = Column(String(500))
    content = Column(Text, nullable=False)
    
    # Author
    author_id = Column(Integer, ForeignKey('users.id'))
    author_name = Column(String(255))
    
    # Categorization
    category_id = Column(Integer, ForeignKey('blog_categories.id'))
    
    # Media
    featured_image = Column(String(500))
    featured_image_alt = Column(String(255))
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    meta_keywords = Column(String(500))
    
    # Status & Visibility
    status = Column(SQLEnum(BlogStatus), default=BlogStatus.DRAFT)
    is_featured = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    
    # Engagement
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    
    # Multi-language
    translations = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("BlogCategory", back_populates="blogs")
    tags = relationship("BlogTag", secondary=blog_tags_assoc, back_populates="blogs")
    author = relationship("User")


class BlogCategory(Base):
    """Blog categories"""
    __tablename__ = "blog_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('blog_categories.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    blogs = relationship("Blog", back_populates="category")
    subcategories = relationship("BlogCategory", backref=backref('parent', remote_side=[id]))


class BlogTag(Base):
    """Blog tags"""
    __tablename__ = "blog_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    blogs = relationship("Blog", secondary=blog_tags_assoc, back_populates="tags")


# ==================== CAREER MODELS ====================

class Career(Base):
    """Job listings"""
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    department = Column(String(100))
    location = Column(String(255))
    job_type = Column(SQLEnum(JobType), nullable=False)
    experience_min = Column(Integer)  # years
    experience_max = Column(Integer)  # years
    
    # Description
    description = Column(Text)
    responsibilities = Column(JSON)
    requirements = Column(JSON)
    preferred_qualifications = Column(JSON)
    benefits = Column(JSON)
    
    # Compensation
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_currency = Column(String(3), default="INR")
    salary_period = Column(String(20), default="annum")  # annum, month, hour
    
    # Status
    is_active = Column(Boolean, default=True)
    application_deadline = Column(DateTime(timezone=True))
    openings_count = Column(Integer, default=1)
    
    # SEO
    slug = Column(String(255), unique=True, index=True)
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    applications = relationship("JobApplication", back_populates="career", cascade="all, delete-orphan")


class JobApplication(Base):
    """Job applications"""
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey('careers.id', ondelete='CASCADE'), nullable=False)
    
    # Applicant Details
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    
    # Qualifications
    highest_qualification = Column(String(255))
    institution = Column(String(255))
    graduation_year = Column(Integer)
    total_experience = Column(Float)  # years
    current_company = Column(String(255))
    current_designation = Column(String(255))
    
    # Resume
    resume_url = Column(String(500), nullable=False)
    resume_file_name = Column(String(255))
    resume_file_size = Column(Integer)
    
    # Additional
    cover_letter = Column(Text)
    portfolio_url = Column(String(500))
    linkedin_url = Column(String(500))
    notice_period = Column(Integer)  # days
    expected_salary = Column(Float)
    
    # Status
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.PENDING)
    review_notes = Column(Text)
    interviewed_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    career = relationship("Career", back_populates="applications")


# ==================== CONTACT MODELS ====================

class Contact(Base):
    """Contact inquiries"""
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    company = Column(String(255))
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Inquiry Type
    inquiry_type = Column(String(100))  # product, service, partnership, etc.
    interested_in = Column(JSON)  # List of products/services
    
    # Status
    status = Column(SQLEnum(ContactStatus), default=ContactStatus.NEW)
    assigned_to = Column(Integer, ForeignKey('users.id'))
    
    # Response
    response = Column(Text)
    responded_at = Column(DateTime(timezone=True))
    responded_by = Column(Integer, ForeignKey('users.id'))
    
    # Spam Detection
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    is_spam = Column(Boolean, default=False)
    spam_score = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assignee = relationship("User", foreign_keys=[assigned_to])
    responder = relationship("User", foreign_keys=[responded_by])


# ==================== FARMER REGISTRATION MODELS ====================

class Farmer(Base):
    """Farmer registration portal"""
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String(50), unique=True, index=True, nullable=False)
    
    # Personal Details
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    father_husband_name = Column(String(255))
    date_of_birth = Column(DateTime(timezone=True))
    gender = Column(String(20))
    
    # Contact
    email = Column(String(255))
    phone = Column(String(20), nullable=False)
    alternate_phone = Column(String(20))
    
    # Address
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    village = Column(String(100), nullable=False)
    taluka = Column(String(100))
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    
    # Farm Details
    total_land_area = Column(Float)  # acres
    irrigated_area = Column(Float)
    rainfed_area = Column(Float)
    soil_type = Column(String(100))
    primary_crops = Column(JSON)
    secondary_crops = Column(JSON)
    
    # Classification
    farmer_type = Column(String(50))  # marginal, small, medium, large
    is_fpo_member = Column(Boolean, default=False)
    fpo_name = Column(String(255))
    
    # Technology Adoption
    uses_weather_station = Column(Boolean, default=False)
    uses_iot_devices = Column(Boolean, default=False)
    interested_in = Column(JSON)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime(timezone=True))
    verified_by = Column(Integer, ForeignKey('users.id'))
    
    # Multi-language
    preferred_language = Column(String(2), default="mr")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    verifier = relationship("User")
    weather_stations = relationship("WeatherStation", back_populates="farmer", cascade="all, delete-orphan")
    training_attendances = relationship("TrainingAttendance", back_populates="farmer", cascade="all, delete-orphan")


# ==================== WEATHER STATION MODELS ====================

class WeatherStation(Base):
    """Weather station installations"""
    __tablename__ = "weather_stations"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(String(50), unique=True, index=True, nullable=False)
    farmer_id = Column(Integer, ForeignKey('farmers.id', ondelete='SET NULL'))
    
    # Installation Details
    installation_date = Column(DateTime(timezone=True))
    location_name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)  # meters
    
    # Hardware
    model = Column(String(100))
    serial_number = Column(String(100))
    firmware_version = Column(String(50))
    
    # Sensors
    sensors_configured = Column(JSON)  # {temperature, humidity, rainfall, etc.}
    
    # Connectivity
    connectivity_type = Column(String(50))  # wifi, cellular, lora, etc.
    sim_number = Column(String(20))
    network_provider = Column(String(100))
    
    # Status
    status = Column(String(50), default="active")  # active, inactive, maintenance
    last_data_received = Column(DateTime(timezone=True))
    battery_level = Column(Float)  # percentage
    
    # Maintenance
    last_maintenance_date = Column(DateTime(timezone=True))
    next_maintenance_date = Column(DateTime(timezone=True))
    maintenance_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    farmer = relationship("Farmer", back_populates="weather_stations")
    readings = relationship("WeatherReading", back_populates="station", cascade="all, delete-orphan")


class WeatherReading(Base):
    """Weather sensor readings"""
    __tablename__ = "weather_readings"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey('weather_stations.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Timestamp
    reading_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Meteorological Data
    temperature = Column(Float)  # Celsius
    humidity = Column(Float)  # Percentage
    pressure = Column(Float)  # hPa
    rainfall = Column(Float)  # mm
    wind_speed = Column(Float)  # km/h
    wind_direction = Column(Integer)  # degrees
    solar_radiation = Column(Float)  # W/m²
    uv_index = Column(Float)
    dew_point = Column(Float)  # Celsius
    soil_temperature = Column(Float)  # Celsius
    soil_moisture = Column(Float)  # Percentage
    leaf_wetness = Column(Boolean)
    
    # Data Quality
    quality_flag = Column(String(20), default="good")  # good, questionable, bad
    validation_errors = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    station = relationship("WeatherStation", back_populates="readings")

    __table_args__ = (
        # Composite index for efficient time-series queries
        {'postgresql_include': ['temperature', 'humidity', 'rainfall']}
    )


# ==================== TRAINING MODELS ====================

class Training(Base):
    """Training programs and workshops"""
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Category
    category = Column(String(100))  # technology, agriculture, entrepreneurship, etc.
    sub_category = Column(String(100))
    
    # Schedule
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))
    duration_days = Column(Integer)
    timing = Column(String(100))  # e.g., "10:00 AM - 4:00 PM"
    
    # Location
    venue = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    is_online = Column(Boolean, default=False)
    online_platform = Column(String(100))
    meeting_link = Column(String(500))
    
    # Capacity
    total_seats = Column(Integer, default=30)
    registered_count = Column(Integer, default=0)
    
    # Fees
    fee_amount = Column(Float, default=0)
    currency = Column(String(3), default="INR")
    includes = Column(JSON)  # meals, materials, certificate, etc.
    
    # Trainer
    trainer_name = Column(String(255))
    trainer_designation = Column(String(255))
    trainer_organization = Column(String(255))
    trainer_bio = Column(Text)
    
    # Eligibility
    eligibility_criteria = Column(JSON)
    target_audience = Column(JSON)
    
    # Curriculum
    agenda = Column(JSON)
    learning_outcomes = Column(JSON)
    
    # Status
    status = Column(String(50), default="upcoming")  # upcoming, ongoing, completed, cancelled
    registration_deadline = Column(DateTime(timezone=True))
    
    # Media
    banner_image = Column(String(500))
    brochure_url = Column(String(500))
    
    # SEO
    slug = Column(String(255), unique=True, index=True)
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    
    # Multi-language
    translations = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    attendees = relationship("TrainingAttendance", back_populates="training", cascade="all, delete-orphan")


class TrainingAttendance(Base):
    """Training registrations and attendance"""
    __tablename__ = "training_attendances"

    id = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey('trainings.id', ondelete='CASCADE'), nullable=False)
    farmer_id = Column(Integer, ForeignKey('farmers.id', ondelete='CASCADE'))
    
    # Participant Details
    participant_name = Column(String(255), nullable=False)
    participant_email = Column(String(255), nullable=False)
    participant_phone = Column(String(20), nullable=False)
    organization = Column(String(255))
    designation = Column(String(100))
    
    # Registration
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    payment_status = Column(String(50), default="pending")  # pending, paid, refunded
    payment_amount = Column(Float)
    payment_mode = Column(String(50))
    transaction_id = Column(String(100))
    
    # Attendance
    is_present = Column(Boolean, default=False)
    check_in_time = Column(DateTime(timezone=True))
    check_out_time = Column(DateTime(timezone=True))
    
    # Feedback
    feedback_rating = Column(Integer)  # 1-5
    feedback_comments = Column(Text)
    would_recommend = Column(Boolean)
    
    # Certificate
    certificate_issued = Column(Boolean, default=False)
    certificate_number = Column(String(100))
    certificate_url = Column(String(500))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    training = relationship("Training", back_populates="attendees")
    farmer = relationship("Farmer", back_populates="training_attendances")


# ==================== TENDER MODELS ====================

class Tender(Base):
    """Government tenders and projects"""
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)
    tender_number = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # Organization
    organization_name = Column(String(255), nullable=False)
    organization_type = Column(String(100))  # central_govt, state_govt, psu, etc.
    department = Column(String(255))
    
    # Category
    category = Column(String(100))  # supply, service, works, consultancy
    sub_category = Column(String(100))
    
    # Timeline
    publish_date = Column(DateTime(timezone=True), nullable=False)
    pre_bid_date = Column(DateTime(timezone=True))
    bid_submission_deadline = Column(DateTime(timezone=True))
    bid_opening_date = Column(DateTime(timezone=True))
    expected_award_date = Column(DateTime(timezone=True))
    contract_duration = Column(String(100))
    
    # Financial
    estimated_value = Column(Float)
    currency = Column(String(3), default="INR")
    emd_amount = Column(Float)  # Earnest Money Deposit
    
    # Eligibility
    eligibility_criteria = Column(JSON)
    required_documents = Column(JSON)
    
    # Location
    location = Column(String(255))
    state = Column(String(100))
    
    # Status
    status = Column(SQLEnum(TenderStatus), default=TenderStatus.UPCOMING)
    award_status = Column(String(50))  # awarded, not_awarded, pending
    awarded_to = Column(String(255))
    awarded_amount = Column(Float)
    
    # Documents
    tender_document_url = Column(String(500))
    corrigendum_urls = Column(JSON)
    
    # Contact
    contact_person = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    
    # Internal Tracking
    is_interested = Column(Boolean, default=False)
    internal_notes = Column(Text)
    assigned_to = Column(Integer, ForeignKey('users.id'))
    bid_prepared = Column(Boolean, default=False)
    bid_submitted = Column(Boolean, default=False)
    bid_submission_date = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assignee = relationship("User")


# ==================== SUPPORT TICKET MODELS ====================

class SupportTicket(Base):
    """Customer support tickets"""
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), unique=True, index=True, nullable=False)
    
    # Customer Details
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    customer_phone = Column(String(20))
    customer_type = Column(String(50))  # farmer, fpo, enterprise, etc.
    
    # Related Entities
    product_id = Column(Integer, ForeignKey('products.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    farmer_id = Column(Integer, ForeignKey('farmers.id'))
    
    # Ticket Details
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100))  # technical, billing, general, etc.
    sub_category = Column(String(100))
    priority = Column(SQLEnum(TicketPriority), default=TicketPriority.MEDIUM)
    
    # Status
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.OPEN)
    
    # Assignment
    assigned_to = Column(Integer, ForeignKey('users.id'))
    department = Column(String(100))
    
    # Resolution
    resolution = Column(Text)
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(Integer, ForeignKey('users.id'))
    
    # SLA
    sla_hours = Column(Integer)  # expected resolution time
    breached = Column(Boolean, default=False)
    
    # Satisfaction
    satisfaction_rating = Column(Integer)  # 1-5
    satisfaction_comments = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    product = relationship("Product")
    project = relationship("Project")
    farmer = relationship("Farmer")
    assignee = relationship("User", foreign_keys=[assigned_to])
    resolver = relationship("User", foreign_keys=[resolved_by])
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan")


class TicketMessage(Base):
    """Ticket conversation messages"""
    __tablename__ = "ticket_messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey('support_tickets.id', ondelete='CASCADE'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'))
    sender_type = Column(String(20), nullable=False)  # customer, support, system
    
    message = Column(Text, nullable=False)
    attachments = Column(JSON)  # list of file URLs
    
    is_internal = Column(Boolean, default=False)  # internal notes not visible to customer
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    ticket = relationship("SupportTicket", back_populates="messages")
    sender = relationship("User")


# ==================== MEDIA & DOWNLOAD MODELS ====================

class MediaGallery(Base):
    """Media gallery items"""
    __tablename__ = "media_gallery"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    
    media_type = Column(String(20), nullable=False)  # image, video, document
    file_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    file_size = Column(Integer)
    
    category = Column(String(100))  # events, products, team, infrastructure, etc.
    tags = Column(JSON)
    
    is_public = Column(Boolean, default=True)
    views_count = Column(Integer, default=0)
    
    meta_data = Column(JSON)  # EXIF data, dimensions, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(Integer, ForeignKey('users.id'))

    # Relationships
    uploader = relationship("User")


class Download(Base):
    """Downloadable resources"""
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    file_url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(20))  # pdf, doc, xls, etc.
    file_size = Column(Integer)
    
    category = Column(String(100))  # brochure, datasheet, report, presentation, etc.
    tags = Column(JSON)
    
    # Access Control
    is_public = Column(Boolean, default=True)
    requires_registration = Column(Boolean, default=False)
    download_limit = Column(Integer)  # null for unlimited
    
    # Statistics
    download_count = Column(Integer, default=0)
    
    # SEO
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    
    # Multi-language
    translations = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_by = Column(Integer, ForeignKey('users.id'))

    # Relationships
    uploader = relationship("User")


# ==================== TESTIMONIAL & PARTNER MODELS ====================

class Testimonial(Base):
    """Client testimonials"""
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(255), nullable=False)
    client_designation = Column(String(255))
    client_organization = Column(String(255))
    client_location = Column(String(255))
    
    testimonial_text = Column(Text, nullable=False)
    rating = Column(Integer, default=5)  # 1-5
    
    # Related Project/Product
    project_id = Column(Integer, ForeignKey('projects.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    
    # Media
    client_photo_url = Column(String(500))
    video_url = Column(String(500))
    
    # Verification
    is_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project = relationship("Project")
    product = relationship("Product")


class Partner(Base):
    """Clients and partners"""
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    partner_type = Column(String(100))  # client, partner, vendor, collaborator, etc.
    
    logo_url = Column(String(500))
    website_url = Column(String(500))
    description = Column(Text)
    
    industry = Column(String(100))
    location = Column(String(255))
    
    partnership_start_date = Column(DateTime(timezone=True))
    partnership_type = Column(String(100))  # strategic, technology, distribution, etc.
    
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    status = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ==================== SEO MODELS ====================

class SEOMetadata(Base):
    """SEO metadata for dynamic pages"""
    __tablename__ = "seo_metadata"

    id = Column(Integer, primary_key=True, index=True)
    page_path = Column(String(255), unique=True, index=True, nullable=False)
    page_type = Column(String(50))  # static, dynamic, product, blog, etc.
    
    meta_title = Column(String(255))
    meta_description = Column(String(500))
    meta_keywords = Column(String(500))
    
    og_title = Column(String(255))
    og_description = Column(String(500))
    og_image = Column(String(500))
    
    twitter_card = Column(String(50), default="summary_large_image")
    twitter_title = Column(String(255))
    twitter_description = Column(String(500))
    twitter_image = Column(String(500))
    
    canonical_url = Column(String(500))
    robots = Column(String(50), default="index, follow")
    
    structured_data = Column(JSON)  # JSON-LD schema
    
    # Multi-language
    language = Column(String(2), default="en")
    translations = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ==================== AUDIT LOG MODEL ====================

class AuditLog(Base):
    """Audit trail for security and compliance"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    
    action = Column(String(100), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, etc.
    resource_type = Column(String(100), nullable=False)  # user, product, blog, etc.
    resource_id = Column(Integer)
    
    old_values = Column(JSON)  # Previous state
    new_values = Column(JSON)  # New state
    
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    request_method = Column(String(10))
    request_path = Column(String(255))
    
    status_code = Column(Integer)
    error_message = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    __table_args__ = (
        # Composite index for efficient auditing queries
        {'postgresql_include': ['action', 'resource_type']}
    )


# ==================== ACHIEVEMENTS COUNTER MODEL ====================

class Achievement(Base):
    """Company achievements for counter display"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    value = Column(Integer, nullable=False)
    suffix = Column(String(20))  # +, K, %, etc.
    prefix = Column(String(20))  # ₹, $, etc.
    
    icon = Column(String(100))
    category = Column(String(100))  # projects, clients, products, etc.
    
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
