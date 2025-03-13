from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
import os
import urllib.parse

# Base declarativa para los modelos
Base = declarative_base()

# Configuración de la base de datos
print("Leyendo variables de entorno...")
RAW_DATABASE_USER = config("DATABASE_USER", cast=str, default="postgres")
print(f"RAW_DATABASE_USER: {RAW_DATABASE_USER!r} (bytes: {RAW_DATABASE_USER.encode('utf-8')!r})")
RAW_DATABASE_PASSWORD = config("DATABASE_PASSWORD", cast=str, default="password")
print(f"RAW_DATABASE_PASSWORD: {RAW_DATABASE_PASSWORD!r} (bytes: {RAW_DATABASE_PASSWORD.encode('utf-8')!r})")
RAW_DATABASE_HOST = config("DATABASE_HOST", cast=str, default="localhost")
print(f"RAW_DATABASE_HOST: {RAW_DATABASE_HOST!r} (bytes: {RAW_DATABASE_HOST.encode('utf-8')!r})")
RAW_DATABASE_PORT = config("DATABASE_PORT", cast=str, default="5432")
print(f"RAW_DATABASE_PORT: {RAW_DATABASE_PORT!r} (bytes: {RAW_DATABASE_PORT.encode('utf-8')!r})")
RAW_DATABASE_DBNAME = config("DATABASE_DBNAME", cast=str, default="weather_db")
print(f"RAW_DATABASE_DBNAME: {RAW_DATABASE_DBNAME!r} (bytes: {RAW_DATABASE_DBNAME.encode('utf-8')!r})")
RAW_DATABASE_SSL_MODE = config("DATABASE_SSL_MODE", default="prefer", cast=str)
print(f"RAW_DATABASE_SSL_MODE: {RAW_DATABASE_SSL_MODE!r} (bytes: {RAW_DATABASE_SSL_MODE.encode('utf-8')!r})")

# Función para depurar y forzar codificación UTF-8
def ensure_utf8(value):
    if value is None:
        return ""
    try:
        return value.encode('utf-8', errors='strict').decode('utf-8', errors='replace')
    except UnicodeEncodeError:
        return value.encode('latin-1', errors='replace').decode('utf-8', errors='replace')

# Aplicar la conversión a todas las variables y codificarlas para URL
DATABASE_USER = urllib.parse.quote_plus(ensure_utf8(RAW_DATABASE_USER))
DATABASE_PASSWORD = urllib.parse.quote_plus(ensure_utf8(RAW_DATABASE_PASSWORD))
DATABASE_HOST = urllib.parse.quote_plus(ensure_utf8(RAW_DATABASE_HOST))
DATABASE_PORT = urllib.parse.quote_plus(ensure_utf8(RAW_DATABASE_PORT))
DATABASE_DBNAME = urllib.parse.quote_plus(ensure_utf8(RAW_DATABASE_DBNAME))
DATABASE_SSL_MODE = urllib.parse.quote_plus(ensure_utf8(RAW_DATABASE_SSL_MODE))

# Depurar: Imprimir los valores después de la conversión y codificación
print(f"DATABASE_USER (encoded): {DATABASE_USER!r}")
print(f"DATABASE_PASSWORD (encoded): {DATABASE_PASSWORD!r}")
print(f"DATABASE_HOST (encoded): {DATABASE_HOST!r}")
print(f"DATABASE_PORT (encoded): {DATABASE_PORT!r}")
print(f"DATABASE_DBNAME (encoded): {DATABASE_DBNAME!r}")
print(f"DATABASE_SSL_MODE (encoded): {DATABASE_SSL_MODE!r}")

# Construir la cadena de conexión
DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DBNAME}"
    f"?sslmode={DATABASE_SSL_MODE}&client_encoding=utf8"
)

print(f"DATABASE_URL: {DATABASE_URL!r} (bytes: {DATABASE_URL.encode('utf-8')!r})")

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"client_encoding": "utf8"})

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para inicializar la base de datos
def init_db():
    # Importar los modelos aquí, después de que Base esté definido
    from app.models.empresa import DbEmpresa
    from app.models.usuari import Usuari
    from app.models.estacio_meteo import EstacioMeteo
    from app.models.measurement import Measurement
    from app.models.tipus_sensor import TipusSensor
    from app.models.sensor import Sensor
    from app.models.config import TblConfig
    from app.models.app_config import AppConfig
    from app.models.measurement import Measurement

    configure_mappers()
    Base.metadata.create_all(bind=engine)