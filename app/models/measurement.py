from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Measurement(Base):
    __tablename__ = "tbl_lectura"

    id = Column(Integer, primary_key=True, index=True)
    id_sensor = Column(Integer, ForeignKey("tbl_sensor.id"), nullable=False)
    valor = Column(Float, nullable=False)
    data_lectura = Column(DateTime, default=func.now())

    sensor = relationship("Sensor", back_populates="measurements")