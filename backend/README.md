# Innovate Enterprise LLP - Backend API

FastAPI-based REST API for Innovate Enterprise LLP website.

## Features

- 🔐 JWT Authentication with refresh tokens
- 👥 Role-Based Access Control (RBAC)
- 📦 Product Management
- 🛠️ Service Catalogue
- 📁 Project Portfolio
- 📝 Blog CMS
- 💼 Career & Job Applications
- 📞 Contact Inquiry System
- 👨‍🌾 Farmer Registration Portal
- 🌤️ Weather Station Integration
- 🎓 Training & Workshop Management
- 📋 Government Tender Tracking
- 🎫 Customer Support Tickets
- 📊 Admin Dashboard
- 🌐 Multi-language Support (English + Marathi)
- 🔒 Security Headers & CSRF Protection
- 📈 Audit Logging

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic
- **Documentation**: Swagger/OpenAPI

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip or poetry

### Installation

1. **Clone the repository**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run database migrations**
```bash
python -m app.db.migrate
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

7. **Access API documentation**
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/           # API route handlers
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── services.py
│   │   ├── projects.py
│   │   ├── blogs.py
│   │   ├── careers.py
│   │   ├── contacts.py
│   │   ├── farmers.py
│   │   ├── weather.py
│   │   ├── training.py
│   │   ├── tenders.py
│   │   ├── tickets.py
│   │   ├── admin.py
│   │   └── uploads.py
│   ├── core/          # Core configurations
│   │   └── config.py
│   ├── db/            # Database configuration
│   │   └── session.py
│   ├── models/        # SQLAlchemy models
│   │   └── __init__.py
│   ├── schemas/       # Pydantic schemas
│   │   └── __init__.py
│   ├── utils/         # Utility functions
│   │   └── security.py
│   └── main.py        # Application entry point
├── tests/             # Test files
├── .env.example       # Environment template
├── requirements.txt   # Dependencies
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user
- `PUT /api/v1/auth/me` - Update profile
- `POST /api/v1/auth/change-password` - Change password

### Products
- `GET /api/v1/products` - List products
- `GET /api/v1/products/{id}` - Get product details
- `POST /api/v1/products` - Create product (admin)
- `PUT /api/v1/products/{id}` - Update product (admin)
- `DELETE /api/v1/products/{id}` - Delete product (admin)

### Services
- `GET /api/v1/services` - List services
- `GET /api/v1/services/{id}` - Get service details

### Projects
- `GET /api/v1/projects` - List projects
- `GET /api/v1/projects/{id}` - Get project details

### Blogs
- `GET /api/v1/blogs` - List blog posts
- `GET /api/v1/blogs/{slug}` - Get blog post
- `POST /api/v1/blogs` - Create blog (admin)

### Careers
- `GET /api/v1/careers` - List job openings
- `POST /api/v1/careers/{id}/apply` - Apply for job

### Contacts
- `POST /api/v1/contacts` - Submit inquiry

### Farmers
- `POST /api/v1/farmers/register` - Register farmer
- `GET /api/v1/farmers` - List farmers (admin)

### Weather Stations
- `GET /api/v1/weather/stations` - List stations
- `POST /api/v1/weather/readings` - Submit readings
- `GET /api/v1/weather/stations/{id}/readings` - Get readings

### Training
- `GET /api/v1/training` - List trainings
- `POST /api/v1/training/{id}/register` - Register for training

### Tenders
- `GET /api/v1/tenders` - List tenders
- `GET /api/v1/tenders/{id}` - Get tender details

### Support Tickets
- `POST /api/v1/tickets` - Create ticket
- `GET /api/v1/tickets` - List tickets (admin)

### Admin
- `GET /api/v1/admin/dashboard` - Dashboard metrics
- `GET /api/v1/admin/users` - User management
- Various CRUD endpoints for all modules

## Database Models

The application includes comprehensive models for:
- Users & Authentication
- Products & Categories
- Services
- Projects & Technologies
- Blogs, Categories & Tags
- Careers & Applications
- Contact Inquiries
- Farmers & Farm Details
- Weather Stations & Readings
- Training Programs & Attendance
- Government Tenders
- Support Tickets & Messages
- Media Gallery & Downloads
- Testimonials & Partners
- SEO Metadata
- Audit Logs

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- CSRF protection
- XSS prevention headers
- SQL injection prevention (via SQLAlchemy)
- Rate limiting support
- Audit logging
- Secure cookie configuration

## Configuration

Key environment variables in `.env`:

```env
# Application
APP_NAME=Innovate Enterprise LLP API
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/innovate_enterprise

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:5173","https://innovateenterprise.com"]

# File Upload
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=/app/uploads

# Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Docker Support

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

## Deployment

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed deployment instructions including:
- Docker containerization
- Nginx reverse proxy
- SSL with Let's Encrypt
- Production best practices

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`
- OpenAPI JSON: `/api/openapi.json`

## License

Proprietary - Innovate Enterprise LLP

## Support

For support, email: support@innovateenterprise.com
