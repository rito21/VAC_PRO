from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Usuari(Base):
    __tablename__ = 'db_usuari'

    id = Column(Integer, primary_key=True, index=True)
    id_empresa = Column(Integer, ForeignKey('db_empresa.id'), nullable=False)
    nom = Column(String(50), nullable=False)
    cognoms = Column(String(50), nullable=False)
    correu_electronic = Column(String(100), unique=True, nullable=False)
    contrasenya = Column(Text, nullable=False)
    data_registre = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    ultim_canvi_contrasenya = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    intents_fallits_login = Column(Integer, default=0)
    bloquejat = Column(Boolean, default=False)
    baixa = Column(Boolean, default=False)
    compte_verificat = Column(Boolean, default=False)

    # Relación con db_empresa
    empresa = relationship("DbEmpresa", back_populates="usuaris")



