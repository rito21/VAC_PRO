from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DbEmpresa(Base):
    __tablename__ = 'db_empresa'

    id = Column(Integer, primary_key=True, index=True)
    nom_empresa = Column(String(100), nullable=False)

    # Relación con la tabla db_usuari
    usuaris = relationship("DbUsuari", back_populates="empresa")
    # Relación con la tabla tbl_config
    configs = relationship("TblConfig", back_populates="empresa")
