from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Usuari(Base):
    __tablename__ = "db_usuari"

    id = Column(Integer, primary_key=True, index=True)
    id_empresa = Column(Integer, ForeignKey("db_empresa.id"), nullable=False)
    correu_electronic = Column(String(100), unique=True, index=True, nullable=False)
    contrasenya = Column(String, nullable=False)
    data_registre = Column(DateTime, default=func.now())
    ultim_canvi_contrasenya = Column(DateTime, default=func.now())
    intents_fallits_login = Column(Integer, default=0)
    bloquejat = Column(Boolean, default=False)
    baixa = Column(Boolean, default=False)
    compte_verificat = Column(Boolean, default=False)
    nom = Column(String(50), nullable=False)
    cognoms = Column(String(50), nullable=False)

    empresa = relationship("DbEmpresa", back_populates="usuaris")