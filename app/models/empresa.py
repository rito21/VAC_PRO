from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class DbEmpresa(Base):
    __tablename__ = 'db_empresa'

    id = Column(Integer, primary_key=True, index=True)
    nom_empresa = Column(String(100), nullable=False, unique=True)

    # Relaciones (usamos strings)
    usuaris = relationship("Usuari", back_populates="empresa")
    estacions = relationship("EstacioMeteo", back_populates="empresa")
    configs = relationship("TblConfig", back_populates="empresa")