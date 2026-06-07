"""Weather Stations API Routes - Live Dashboard Integration"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.models import WeatherStation, WeatherReading
from app.schemas import WeatherReadingCreate, WeatherReadingResponse, WeatherStationResponse
router = APIRouter()

@router.get("/stations", response_model=list[WeatherStationResponse])
async def list_stations(db: Session = Depends(get_db)):
    return db.query(WeatherStation).filter(WeatherStation.status == "active").all()

@router.post("/readings", status_code=201)
async def submit_reading(reading: WeatherReadingCreate, db: Session = Depends(get_db)):
    db_reading = WeatherReading(**reading.dict())
    db.add(db_reading)
    station = db.query(WeatherStation).get(reading.station_id)
    if station:
        station.last_data_received = datetime.utcnow()
    db.commit()
    return {"message": "Reading recorded successfully"}

@router.get("/stations/{station_id}/readings", response_model=list[WeatherReadingResponse])
async def get_station_readings(station_id: int, db: Session = Depends(get_db)):
    return db.query(WeatherReading).filter(WeatherReading.station_id == station_id).order_by(WeatherReading.reading_timestamp.desc()).limit(100).all()
