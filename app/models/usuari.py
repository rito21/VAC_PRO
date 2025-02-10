from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base


class Usuari(Base):
    """
    Model de dades per a la taula d'usuaris
    """
    __tablename__ = 'tbl_usuaris'

    id = Column(Integer, primary_key=True, index=True)
    correu_electronic = Column(String, unique=True, index=True)
    contrasenya = Column(String)
    es_actiu = Column(Boolean, default=True)
    data_creacio = Column(DateTime, default=datetime.now(timezone.utc))
    es_admin = Column(Boolean, default=False)
    intents_login = Column(Integer, default=0)
    nom_complet = Column(String)
