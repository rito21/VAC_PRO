from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Usuari(Base):
    __tablename__ = "db_usuari"

    id = Column(Integer, primary_key=True, index=True)
    id_empresa = Column(Integer, ForeignKey("db_empresa.id"), nullable=False)
    nom = Column(String(50), nullable=False)
    cognoms = Column(String(50), nullable=False)
    correu_electronic = Column(String(100), unique=True, index=True, nullable=False)
    contrasenya = Column(String, nullable=False)
    data_registre = Column(DateTime, default=datetime.utcnow)
    ultim_canvi_contrasenya = Column(DateTime, default=datetime.utcnow)
    intents_fallits_login = Column(Integer, default=0)
    bloquejat = Column(Boolean, default=False)
    baixa = Column(Boolean, default=False)
    compte_verificat = Column(Boolean, default=False)

    # Relaciones
    empresa = relationship("DbEmpresa", back_populates="usuaris")
    devices = relationship("Device", back_populates="usuari")