"""
Services endpoints
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.service import Service

router = APIRouter()


@router.get("")
async def list_services(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all services"""
    
    query = db.query(Service)
    
    if category:
        query = query.filter(Service.category == category)
    
    offset = (page - 1) * page_size
    services = query.offset(offset).limit(page_size).all()
    total = query.count()
    
    return {
        "items": services,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{service_id}")
async def get_service(service_id: str, db: Session = Depends(get_db)):
    """Get a specific service"""
    
    service = db.query(Service).filter(Service.id == service_id).first()
    
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return service
