from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    id_sensor = Column(Integer, ForeignKey("tbl_sensor.id"), nullable=False)

    # Relación con Sensor
    sensor = relationship("Sensor", back_populates="measurements")