"""
API v1 Router - Combines all endpoint routers
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    products,
    services,
    projects,
    blogs,
    careers,
    contacts,
    weather,
    farmers,
    tickets,
    training,
    tenders,
    admin,
)

# Create main API router
api_router = APIRouter()

# Authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User management endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Product catalogue endpoints
api_router.include_router(products.router, prefix="/products", tags=["Products"])

# Services endpoints
api_router.include_router(services.router, prefix="/services", tags=["Services"])

# Project portfolio endpoints
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])

# Blog CMS endpoints
api_router.include_router(blogs.router, prefix="/blogs", tags=["Blogs"])
api_router.include_router(blogs.router, prefix="/blog-categories", tags=["Blog Categories"])
api_router.include_router(blogs.router, prefix="/blog-tags", tags=["Blog Tags"])

# Career endpoints
api_router.include_router(careers.router, prefix="/careers", tags=["Careers"])
api_router.include_router(careers.router, prefix="/job-applications", tags=["Job Applications"])

# Contact endpoints
api_router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])

# Weather station endpoints
api_router.include_router(weather.router, prefix="/weather-stations", tags=["Weather Stations"])
api_router.include_router(weather.router, prefix="/weather-readings", tags=["Weather Readings"])

# Farmer portal endpoints
api_router.include_router(farmers.router, prefix="/farmers", tags=["Farmers"])

# Support ticket endpoints
api_router.include_router(tickets.router, prefix="/tickets", tags=["Support Tickets"])

# Training endpoints
api_router.include_router(training.router, prefix="/training-events", tags=["Training Events"])
api_router.include_router(training.router, prefix="/training-registrations", tags=["Training Registrations"])

# Government tender endpoints
api_router.include_router(tenders.router, prefix="/tenders", tags=["Government Tenders"])

# Admin dashboard endpoints
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
