from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DbEstacioMeteo(Base):
    __tablename__ = 'tbl_estacio_meteo'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    descripcio = Column(String)
    ubicacio = Column(String(255))
    id_empresa = Column(Integer, ForeignKey("db_empresa.id"), nullable=False)
    estat = Column(Boolean, default=True)
    data_creacio = Column(DateTime, default=datetime.utcnow)
    ultima_connexio = Column(DateTime)
    ip_address = Column(String(45))
    mac_address = Column(String(17))
    versio_firmware = Column(String(50))

    # Relaciones
    empresa = relationship("DbEmpresa", back_populates="estacions")
    sensors = relationship("DbSensor", back_populates="estacio") 