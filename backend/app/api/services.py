"""
Services API Routes
CRUD operations for service offerings
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.models import Service
from app.schemas import ServiceCreate, ServiceUpdate, ServiceResponse
from app.utils.security import get_current_active_user

router = APIRouter()


@router.get("/", response_model=list[ServiceResponse])
async def list_services(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all services with optional category filter"""
    query = db.query(Service).filter(Service.status == True)
    if category:
        query = query.filter(Service.category == category)
    return query.all()


@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Get service details by ID"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service
