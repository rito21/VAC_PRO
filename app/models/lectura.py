from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DbLectura(Base):
    __tablename__ = 'tbl_lectura'

    id = Column(Integer, primary_key=True, index=True)
    id_sensor = Column(Integer, ForeignKey("tbl_sensor.id"), nullable=False)
    valor = Column(Float, nullable=False)
    data_lectura = Column(DateTime, nullable=False)
    qualitat_lectura = Column(Integer)
    bateria = Column(Float)
    rssi = Column(Integer)
    metadata = Column(JSON)

    # Relación con sensor
    sensor = relationship("DbSensor", back_populates="lectures") 