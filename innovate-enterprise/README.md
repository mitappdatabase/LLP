# Innovate Enterprise LLP - Production Website

## Project Structure

```
innovate-enterprise/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── store/
│   │   ├── utils/
│   │   ├── assets/
│   │   └── locales/
│   └── public/
├── docker/
│   ├── nginx/
│   ├── postgres/
│   └── backup/
└── docs/
```

## Tech Stack

- **Frontend**: React 19 + Vite + Material UI
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **State Management**: React Query
- **Form Validation**: React Hook Form + Zod
- **Deployment**: Docker + Nginx
- **SSL**: Let's Encrypt

## Features

- Multi-language support (English + Marathi)
- Product catalogue with PDFs
- Project case studies
- Weather station live dashboard
- KrushiNetra AI portal integration
- Customer support ticket system
- Farmer registration portal
- Government tender showcase
- Training & workshop registration
- Blog CMS
- Career management
- Contact inquiry system
- Admin dashboard with analytics

## Quick Start

```bash
# Start all services
docker-compose up -d

# Access frontend
http://localhost:3000

# Access backend API
http://localhost:8000

# Access Swagger docs
http://localhost:8000/docs

# Access admin panel
http://localhost:3000/admin
```

## Documentation

- [Database Schema](docs/database-schema.md)
- [ER Diagram](docs/er-diagram.md)
- [API Documentation](docs/api-documentation.md)
- [Deployment Guide](docs/deployment-guide.md)
- [Security Checklist](docs/security-checklist.md)
