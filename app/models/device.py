from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    id_usuari = Column(Integer, ForeignKey("db_usuari.id"), nullable=False)  # Añadimos ForeignKey a Usuari

    # Relaciones
    usuari = relationship("Usuari", back_populates="devices")