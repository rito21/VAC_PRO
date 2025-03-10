from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DbSensor(Base):
    __tablename__ = 'tbl_sensor'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    id_estacio = Column(Integer, ForeignKey("tbl_estacio_meteo.id"), nullable=False)
    id_tipus_sensor = Column(Integer, ForeignKey("tbl_tipus_sensor.id"), nullable=False)
    estat = Column(Boolean, default=True)
    data_creacio = Column(DateTime, default=datetime.utcnow)
    ultima_lectura = Column(DateTime)
    calibracio = Column(JSON)

    # Relaciones
    tipus_sensor = relationship("DbTipusSensor", back_populates="sensors")
    estacio = relationship("DbEstacioMeteo", back_populates="sensors")
    lectures = relationship("DbLectura", back_populates="sensor") 