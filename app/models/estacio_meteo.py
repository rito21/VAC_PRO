from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class EstacioMeteo(Base):
    __tablename__ = "tbl_estacio_meteo"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    descripcio = Column(String)
    ubicacio = Column(String(255))
    id_empresa = Column(Integer, ForeignKey("db_empresa.id"), nullable=False)
    estat = Column(Boolean, default=True)
    data_creacio = Column(DateTime, default=func.now())
    ultima_connexio = Column(DateTime)
    ip_address = Column(String(45))
    mac_address = Column(String(17), unique=True)
    versio_firmware = Column(String(50))
    latitude = Column(Float)
    longitude = Column(Float)

    empresa = relationship("DbEmpresa", back_populates="estacions_meteo")
    sensors = relationship("Sensor", back_populates="estacio_meteo")