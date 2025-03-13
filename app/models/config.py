from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TblConfig(Base):
    __tablename__ = "tbl_config"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("db_empresa.id"), nullable=False, unique=True)
    longitud_minima_contrasenya = Column(Integer, default=8)
    intents_fallits_maxims = Column(Integer, default=5)
    data_ultim_canvi_contrasenya = Column(DateTime, default=datetime.utcnow)

    # Relación con DbEmpresa (usamos string)
    empresa = relationship("DbEmpresa", back_populates="configs")