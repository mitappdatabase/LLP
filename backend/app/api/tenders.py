"""Tenders API Routes - Government Project Showcase"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Tender, TenderStatus
from app.schemas import TenderResponse
router = APIRouter()

@router.get("/", response_model=list[TenderResponse])
async def list_tenders(db: Session = Depends(get_db)):
    return db.query(Tender).filter(Tender.status == TenderStatus.ACTIVE).all()

@router.get("/{tender_id}", response_model=TenderResponse)
async def get_tender(tender_id: int, db: Session = Depends(get_db)):
    return db.query(Tender).filter(Tender.id == tender_id).first()
