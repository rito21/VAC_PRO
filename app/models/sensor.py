from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Sensor(Base):
    __tablename__ = "tbl_sensor"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    id_estacio = Column(Integer, ForeignKey("tbl_estacio_meteo.id"), nullable=False)
    id_tipus_sensor = Column(Integer, ForeignKey("tbl_tipus_sensor.id"), nullable=False)
    estat = Column(Boolean, default=True)
    data_creacio = Column(DateTime, default=datetime.utcnow)
    ultima_lectura = Column(DateTime)
    calibracio = Column(JSON)

    __table_args__ = ({"schema": None},)

    # Relaciones
    tipus_sensor = relationship("TipusSensor", back_populates="sensors")
    estacio = relationship("EstacioMeteo", back_populates="sensors")
    lectures = relationship("Lectura", back_populates="sensor")  # Relación con Lectura
    measurements = relationship("Measurement", back_populates="sensor")  # Añadimos la relación con Measurement