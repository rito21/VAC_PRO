from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class TblConfig(Base):
    __tablename__ = 'tbl_config'

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey('db_empresa.id'), nullable=False)
    longitud_minima_contrasenya = Column(Integer, default=8)
    intents_fallits_maxims = Column(Integer, default=5)
    data_ultim_canvi_contrasenya = Column(TIMESTAMP, server_default=func.now())

    # Relación con la tabla db_empresa
    empresa = relationship("DbEmpresa", back_populates="configs")
