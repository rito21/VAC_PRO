from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from decouple import config
import urllib.parse

# Configuración de la URL de la base de datos desde .env
DATABASE_USER = config("DATABASE_USER")
DATABASE_PASSWORD = config("DATABASE_PASSWORD")
DATABASE_HOST = config("DATABASE_HOST")
DATABASE_PORT = config("DATABASE_PORT")
DATABASE_DBNAME = config("DATABASE_DBNAME")
DATABASE_SSL_MODE = config("DATABASE_SSL_MODE", default="prefer")

# Codificamos usuario y contraseña
DATABASE_USER_ENCODED = urllib.parse.quote(DATABASE_USER)
DATABASE_PASSWORD_ENCODED = urllib.parse.quote(DATABASE_PASSWORD)

# Usamos psycopg explícitamente
DATABASE_URL = f"postgresql+psycopg://{DATABASE_USER_ENCODED}:{DATABASE_PASSWORD_ENCODED}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DBNAME}?sslmode={DATABASE_SSL_MODE}"

# Configuramos el engine con parámetros para manejar reconexiones y estabilidad
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": DATABASE_SSL_MODE},
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    pool_size=5,  # Tamaño del pool de conexiones
    max_overflow=10,  # Máximo de conexiones adicionales
    pool_timeout=30,  # Tiempo máximo de espera para una conexión
    pool_recycle=1800,  # Recicla conexiones cada 30 minutos para evitar timeouts
    echo=True  # Habilita logs detallados de SQLAlchemy para depurar
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """Inicializa la base de datos con una empresa predeterminada y su configuración."""
    from app.models.empresa import DbEmpresa
    from app.models.usuari import Usuari
    from app.models.config import TblConfig

    # Verificamos si las tablas ya existen
    inspector = inspect(engine)
    tables_exist = inspector.has_table("db_empresa")

    # Creamos las tablas si no existen
    if not tables_exist:
        print("Creando tablas...")
        Base.metadata.create_all(bind=engine)

    # Inicializamos datos
    with SessionLocal() as db:
        # Verificar si la empresa existe
        empresa = db.query(DbEmpresa).filter(DbEmpresa.id == 1).first()
        print(f"Empresa encontrada: {empresa}")
        if not empresa:
            print("Creando empresa predeterminada (id=1)...")
            empresa = DbEmpresa(id=1, nom_empresa="Empresa Única")
            db.add(empresa)
            try:
                db.commit()
                db.refresh(empresa)
                print("Empresa creada correctamente:", empresa.id)
            except Exception as e:
                print(f"Error al crear empresa: {e}")
                db.rollback()
                raise

        # Verificar si la configuración existe
        config = db.query(TblConfig).filter(TblConfig.empresa == 1).first()
        print(f"Configuración encontrada: {config}")
        if not config:
            print("Creando configuración predeterminada para empresa 1...")
            config = TblConfig(
                empresa=1,
                longitud_minima_contrasenya=8,
                intents_fallits_maxims=5
            )
            db.add(config)
            try:
                db.commit()
                print("Configuración creada correctamente:", config.id)
            except Exception as e:
                print(f"Error al crear configuración: {e}")
                db.rollback()
                raise


def get_db():
    """Dependencia para obtener una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Llamamos a init_db al importar el módulo
init_db()