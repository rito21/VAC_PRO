from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Sensor(Base):
    __tablename__ = "tbl_sensor"

    id = Column(Integer, primary_key=True, index=True)
    id_estacio = Column(Integer, ForeignKey("tbl_estacio_meteo.id"), nullable=False)
    id_tipus_sensor = Column(Integer, ForeignKey("tbl_tipus_sensor.id"), nullable=False)
    nom = Column(String(50), nullable=False)
    estat = Column(Boolean, default=True)
    data_creacio = Column(DateTime, default=func.now())
    ultima_lectura = Column(DateTime)
    calibracio = Column(JSON)

    estacio_meteo = relationship("EstacioMeteo", back_populates="sensors")
    tipus_sensor = relationship("TipusSensor", back_populates="sensors")
    measurements = relationship("Measurement", back_populates="sensor")