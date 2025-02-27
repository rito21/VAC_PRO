from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class TblConfig(Base):
    __tablename__ = "tbl_config"

    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(Integer, ForeignKey("db_empresa.id"), nullable=False)
    longitud_minima_contrasenya = Column(Integer, default=8)
    intents_fallits_maxims = Column(Integer, default=5)
    data_ultim_canvi_contrasenya = Column(DateTime, default=func.now())

    empresa_rel = relationship("DbEmpresa", back_populates="configs")