"""Training API Routes - Workshop Registration System"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Training
from app.schemas import TrainingResponse
router = APIRouter()

@router.get("/", response_model=list[TrainingResponse])
async def list_trainings(db: Session = Depends(get_db)):
    return db.query(Training).filter(Training.status == "upcoming").all()

@router.get("/{training_id}", response_model=TrainingResponse)
async def get_training(training_id: int, db: Session = Depends(get_db)):
    return db.query(Training).filter(Training.id == training_id).first()
