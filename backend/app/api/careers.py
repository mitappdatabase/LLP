"""Careers API Routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Career
from app.schemas import CareerResponse
router = APIRouter()

@router.get("/", response_model=list[CareerResponse])
async def list_careers(db: Session = Depends(get_db)):
    return db.query(Career).filter(Career.is_active == True).all()

@router.get("/{career_id}", response_model=CareerResponse)
async def get_career(career_id: int, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Job not found")
    return career
