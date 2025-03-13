from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class EstacioMeteo(Base):
    __tablename__ = "tbl_estacio_meteo"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    descripcio = Column(String(255))
    ubicacio = Column(String(255))
    id_empresa = Column(Integer, ForeignKey("db_empresa.id"), nullable=False)
    estat = Column(Boolean, default=True)
    data_creacio = Column(DateTime, default=datetime.utcnow)
    ultima_connexio = Column(DateTime)
    ip_address = Column(String(45))
    mac_address = Column(String(17), unique=True)
    versio_firmware = Column(String(50))
    latitude = Column(Float(10, 7))
    longitude = Column(Float(10, 7))

    # Relaciones (usamos strings para evitar importaciones circulares)
    empresa = relationship("DbEmpresa", back_populates="estacions")
    sensors = relationship("Sensor", back_populates="estacio")