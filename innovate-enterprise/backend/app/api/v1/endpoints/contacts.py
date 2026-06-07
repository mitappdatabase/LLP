"""
Contact inquiry endpoints
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from app.core.security import get_current_user, check_permission

router = APIRouter()


@router.get("", response_model=list)
async def list_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all contact inquiries (Admin only)"""
    
    if not check_permission(current_user, "contacts", "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    query = db.query(Contact)
    
    if status:
        query = query.filter(Contact.status == status)
    
    query = query.order_by(Contact.created_at.desc())
    
    offset = (page - 1) * page_size
    contacts = query.offset(offset).limit(page_size).all()
    total = query.count()
    
    return {
        "items": contacts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact_inquiry(
    contact_data: ContactCreate,
    db: Session = Depends(get_db),
):
    """Submit a contact inquiry (Public)"""
    
    contact = Contact(
        name=contact_data.name,
        company=contact_data.company,
        email=contact_data.email,
        mobile=contact_data.mobile,
        subject=contact_data.subject,
        message=contact_data.message,
    )
    
    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    # TODO: Send email notification to admin
    
    return contact


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific contact inquiry (Admin only)"""
    
    if not check_permission(current_user, "contacts", "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact inquiry not found"
        )
    
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: str,
    contact_data: ContactUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a contact inquiry (Admin only)"""
    
    if not check_permission(current_user, "contacts", "update"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact inquiry not found"
        )
    
    update_data = contact_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    
    return contact
