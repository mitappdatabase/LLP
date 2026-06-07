"""
Admin dashboard endpoints
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models.user import User
from app.models.product import Product
from app.models.blog import Blog
from app.models.contact import Contact
from app.models.career import JobApplication
from app.models.weather import WeatherReading
from app.core.security import get_current_user

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get dashboard statistics (Admin only)"""
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Count statistics
    total_products = db.query(Product).count()
    active_products = db.query(Product).filter(Product.status == "active").count()
    
    total_blogs = db.query(Blog).count()
    published_blogs = db.query(Blog).filter(Blog.is_published == True).count()
    
    total_contacts = db.query(Contact).count()
    new_contacts = db.query(Contact).filter(Contact.status == "new").count()
    
    total_applications = db.query(JobApplication).count()
    pending_applications = db.query(JobApplication).filter(JobApplication.status == "pending").count()
    
    # Recent activity
    recent_contacts = db.query(Contact).order_by(Contact.created_at.desc()).limit(5).all()
    recent_applications = db.query(JobApplication).order_by(JobApplication.applied_at.desc()).limit(5).all()
    
    # Weather station stats (if available)
    weather_stations_count = db.query(func.count(func.distinct(WeatherReading.station_id))).scalar() or 0
    latest_reading = db.query(WeatherReading).order_by(WeatherReading.recorded_at.desc()).first()
    
    return {
        "products": {
            "total": total_products,
            "active": active_products,
        },
        "blogs": {
            "total": total_blogs,
            "published": published_blogs,
        },
        "contacts": {
            "total": total_contacts,
            "new": new_contacts,
        },
        "applications": {
            "total": total_applications,
            "pending": pending_applications,
        },
        "weather": {
            "stations": weather_stations_count,
            "last_reading": latest_reading.recorded_at if latest_reading else None,
        },
        "recent_activity": {
            "contacts": recent_contacts,
            "applications": recent_applications,
        }
    }


@router.get("/analytics")
async def get_analytics(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get analytics data for the specified period (Admin only)"""
    
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Contacts per day
    contacts_data = db.query(
        func.date(Contact.created_at).label('date'),
        func.count(Contact.id).label('count')
    ).filter(
        Contact.created_at >= start_date
    ).group_by(
        func.date(Contact.created_at)
    ).all()
    
    # Applications per day
    applications_data = db.query(
        func.date(JobApplication.applied_at).label('date'),
        func.count(JobApplication.id).label('count')
    ).filter(
        JobApplication.applied_at >= start_date
    ).group_by(
        func.date(JobApplication.applied_at)
    ).all()
    
    return {
        "period_days": days,
        "contacts": [{"date": str(d), "count": c} for d, c in contacts_data],
        "applications": [{"date": str(d), "count": c} for d, c in applications_data],
    }
