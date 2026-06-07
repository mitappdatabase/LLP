"""Farmers API Routes - Farmer Registration Portal"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Farmer
from app.schemas import FarmerCreate, FarmerResponse
router = APIRouter()

@router.post("/register", response_model=FarmerResponse, status_code=201)
async def register_farmer(farmer: FarmerCreate, db: Session = Depends(get_db)):
    reg_num = f"FRM{db.query(Farmer).count() + 1:06d}"
    db_farmer = Farmer(**farmer.dict(), registration_number=reg_num)
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer
