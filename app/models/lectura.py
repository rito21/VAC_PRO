from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Lectura(Base):
    __tablename__ = "tbl_lectura"

    id = Column(Integer, primary_key=True, index=True)
    id_sensor = Column(Integer, ForeignKey("tbl_sensor.id"), nullable=False)
    valor = Column(Float(10, 2), nullable=False)
    data_lectura = Column(DateTime, nullable=False)
    qualitat_lectura = Column(Integer, CheckConstraint('qualitat_lectura >= 0 AND qualitat_lectura <= 100'))
    bateria = Column(Float(5, 2))
    rssi = Column(Integer)
    dades_addicionals = Column(JSON)
    sincronitzat = Column(Boolean, default=False)

    # Relación con Sensor
    sensor = relationship("Sensor", back_populates="lectures")