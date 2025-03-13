from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TipusSensor(Base):
    __tablename__ = "tbl_tipus_sensor"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False, unique=True)
    descripcio = Column(String(255))
    unitat = Column(String(20), nullable=False)
    data_creacio = Column(DateTime, default=datetime.utcnow)

    # Relación con sensores (usamos string para evitar importación circular)
    sensors = relationship("Sensor", back_populates="tipus_sensor")