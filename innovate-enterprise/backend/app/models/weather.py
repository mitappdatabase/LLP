"""
Weather station and reading models
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Numeric, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.session import Base


class WeatherStation(Base):
    """Weather station model for IoT devices"""
    
    __tablename__ = "weather_stations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255))
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    altitude = Column(Numeric(10, 2))
    sensor_config = Column(JSONB, default=dict)
    is_active = Column(Boolean, default=True, index=True)
    last_reading = Column(DateTime(timezone=True))
    maintenance_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    readings = relationship(
        "WeatherReading", 
        back_populates="station",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<WeatherStation {self.name}>"


class WeatherReading(Base):
    """Weather reading model for sensor data"""
    
    __tablename__ = "weather_readings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("weather_stations.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    temperature = Column(Numeric(5, 2))  # Celsius
    humidity = Column(Numeric(5, 2))  # Percentage
    pressure = Column(Numeric(7, 2))  # hPa
    rainfall = Column(Numeric(6, 2))  # mm
    wind_speed = Column(Numeric(6, 2))  # km/h
    wind_direction = Column(Integer)  # Degrees 0-360
    solar_radiation = Column(Numeric(7, 2))  # W/m²
    soil_temperature = Column(Numeric(5, 2))  # Celsius
    soil_moisture = Column(Numeric(5, 2))  # Percentage
    additional_data = Column(JSONB, default=dict)
    recorded_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    station = relationship("WeatherStation", back_populates="readings")
    
    def __repr__(self):
        return f"<WeatherReading {self.station_id} at {self.recorded_at}>"
