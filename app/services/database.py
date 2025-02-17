from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Codifiquem la contrasenya per evitar problemes amb caràcters especials
database_password = settings.DATABASE_PASSWORD

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DATABASE_USER}:{database_password}"
    f"@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_DBNAME}"
    f"?sslmode={settings.DATABASE_SSL_MODE}"
)

# Creació del motor de base de dades
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Creació de la sessió local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaració de la base per als models
Base = declarative_base()


# Definició del model per a db_empresa
class DbEmpresa(Base):
    __tablename__ = 'db_empresa'

    id = Column(Integer, primary_key=True, index=True)
    nom_empresa = Column(String(100), nullable=False)

    # Relació amb db_usuari
    usuaris = relationship("DbUsuari", back_populates="empresa")


# Definició del model per a db_usuari
class DbUsuari(Base):
    __tablename__ = 'db_usuari'

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey('db_empresa.id'), nullable=False)
    nom = Column(String(50), nullable=False)
    cognoms = Column(String(50), nullable=False)
    correu = Column(String(100), unique=True, nullable=False)
    contrasenya = Column(Text, nullable=False)  # Almacenar el hash de la contrasenya
    data_registre = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    ultim_canvi_contrasenya = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    intents_fallits_login = Column(Integer, default=0)
    bloquejat = Column(Boolean, default=False)
    baixa = Column(Boolean, default=False)
    compte_verificat = Column(Boolean, default=False)

    # Relació amb db_empresa
    empresa = relationship("DbEmpresa", back_populates="usuaris")


# Definició del model per a tbl_config
class TblConfig(Base):
    __tablename__ = 'tbl_config'

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey('db_empresa.id'), nullable=False)
    longitud_minima_contrasenya = Column(Integer, default=8)
    intents_fallits_maxims = Column(Integer, default=5)
    data_ultim_canvi_contrasenya = Column(TIMESTAMP, server_default=func.now())

    # Relació amb db_empresa
    empresa = relationship("DbEmpresa", back_populates="configs")


# Definició del model per a app_config
class AppConfig(Base):
    __tablename__ = 'app_config'

    id = Column(Integer, primary_key=True, index=True)
    smtp_server = Column(String(255), nullable=False)
    smtp_user = Column(String(255), nullable=False)
    smtp_password = Column(Text, nullable=False)


# Relació entre db_empresa i tbl_config
DbEmpresa.configs = relationship("TblConfig", back_populates="empresa")
