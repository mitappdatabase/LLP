"""
FastAPI Main Application Entry Point
Innovate Enterprise LLP Backend API
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time

from app.core.config import settings
from app.db.session import init_db
from app.utils.security import SecurityHeaders


# ==================== LIFESPAN MANAGER ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events"""
    # Startup
    print("🚀 Starting Innovate Enterprise LLP API...")
    print(f"📍 Environment: {'Development' if settings.DEBUG else 'Production'}")
    print(f"📊 Version: {settings.APP_VERSION}")
    
    # Initialize database tables
    init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("👋 Shutting down Innovate Enterprise LLP API...")


# ==================== APPLICATION FACTORY ====================

def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register exception handlers
    register_exception_handlers(app)
    
    # Register middleware
    register_middleware(app)
    
    # Include routers
    include_routers(app)
    
    return app


def register_exception_handlers(app: FastAPI):
    """Register global exception handlers"""
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors"""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": "Validation Error",
                "detail": errors,
                "status_code": 422
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unhandled exceptions"""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "Internal Server Error",
                "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
                "status_code": 500
            }
        )


def register_middleware(app: FastAPI):
    """Register custom middleware"""
    
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        """Add security headers to all responses"""
        response = await call_next(request)
        
        # Add security headers
        for header, value in SecurityHeaders.get_headers().items():
            response.headers[header] = value
        
        # Add request ID for tracing
        response.headers["X-Request-ID"] = f"req_{int(time.time() * 1000)}"
        
        return response
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log incoming requests (in production, use proper logging)"""
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        if settings.DEBUG:
            print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
        
        return response


def include_routers(app: FastAPI):
    """Include API routers"""
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "timestamp": time.time()
        }
    
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information"""
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": settings.APP_DESCRIPTION,
            "docs": "/api/docs",
            "redoc": "/api/redoc",
            "openapi": "/api/openapi.json"
        }
    
    # Import and include API routers
    from app.api import auth, products, services, projects, blogs, careers, contacts, farmers, weather, training, tenders, tickets, admin, uploads
    
    # API version prefix
    api_prefix = "/api/v1"
    
    app.include_router(auth.router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
    app.include_router(products.router, prefix=f"{api_prefix}/products", tags=["Products"])
    app.include_router(services.router, prefix=f"{api_prefix}/services", tags=["Services"])
    app.include_router(projects.router, prefix=f"{api_prefix}/projects", tags=["Projects"])
    app.include_router(blogs.router, prefix=f"{api_prefix}/blogs", tags=["Blogs"])
    app.include_router(careers.router, prefix=f"{api_prefix}/careers", tags=["Careers"])
    app.include_router(contacts.router, prefix=f"{api_prefix}/contacts", tags=["Contacts"])
    app.include_router(farmers.router, prefix=f"{api_prefix}/farmers", tags=["Farmers"])
    app.include_router(weather.router, prefix=f"{api_prefix}/weather", tags=["Weather Stations"])
    app.include_router(training.router, prefix=f"{api_prefix}/training", tags=["Training"])
    app.include_router(tenders.router, prefix=f"{api_prefix}/tenders", tags=["Tenders"])
    app.include_router(tickets.router, prefix=f"{api_prefix}/tickets", tags=["Support Tickets"])
    app.include_router(admin.router, prefix=f"{api_prefix}/admin", tags=["Admin"])
    app.include_router(uploads.router, prefix=f"{api_prefix}/uploads", tags=["Uploads"])


# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else 4,
    )
