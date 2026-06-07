"""Contacts API Routes"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Contact
from app.schemas import ContactCreate, ContactResponse
from app.utils.security import get_client_ip

router = APIRouter()

@router.post("/", response_model=ContactResponse, status_code=201)
async def create_contact(
    contact: ContactCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    db_contact = Contact(
        **contact.dict(),
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent")
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
