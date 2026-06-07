"""Support Tickets API Routes - Customer Support System"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import SupportTicket
from app.schemas import SupportTicketCreate, SupportTicketResponse
router = APIRouter()

@router.post("/", response_model=SupportTicketResponse, status_code=201)
async def create_ticket(ticket: SupportTicketCreate, db: Session = Depends(get_db)):
    ticket_num = f"TKT{db.query(SupportTicket).count() + 1:06d}"
    db_ticket = SupportTicket(**ticket.dict(), ticket_number=ticket_num)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
