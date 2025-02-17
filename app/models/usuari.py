from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Usuari(Base):
    """
    Model de dades per a la taula d'usuaris
    """
    __tablename__ = 'db_usuari'

    id = Column(Integer, primary_key=True, index=True)
    empresa = Column(Integer, ForeignKey, nullable=False)  # Clau forana a db_empresa
    nom = Column(String(50), nullable=False)
    cognoms = Column(String(50), nullable=False)
    correu = Column(String(100), unique=True, nullable=False, index=True)
    contrasenya = Column(Text, nullable=False)  # Hash de la contrasenya
    data_registre = Column(DateTime, default=func.now())  # Data i hora de registre
    ultim_canvi_contrasenya = Column(DateTime, default=func.now())  # Últim canvi de contrasenya
    intents_fallits_login = Column(Integer, default=0)  # Intents fallits de login
    bloquejat = Column(Boolean, default=False)  # Indica si el compte està bloquejat
    baixa = Column(Boolean, default=False)  # Indica si el compte està donat de baixa
    compte_verificat = Column(Boolean, default=False)  # Indica si el compte ha estat verificat

    def nom_complet(self):
        """Retorna el nom complet de l'usuari."""
        return f"{self.nom} {self.cognoms}"
