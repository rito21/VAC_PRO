from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DbTipusSensor(Base):
    __tablename__ = 'tbl_tipus_sensor'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    descripcio = Column(String)
    unitat = Column(String(20), nullable=False)
    data_creacio = Column(DateTime, default=datetime.utcnow)

    # Relación con sensores
    sensors = relationship("DbSensor", back_populates="tipus_sensor") 