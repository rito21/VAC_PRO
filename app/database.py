from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuración de la URL de la base de datos (ajusta según tu base de datos)
DATABASE_URL = "sqlite:///./test.db"  # Para SQLite
# DATABASE_URL = "postgresql://user:password@localhost/dbname"  # Para PostgreSQL
# DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"  # Para MySQL

# Creación del motor de base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}  # Evita errores en SQLite
)

# Creación de la sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos de SQLAlchemy
Base = declarative_base()

def get_db():
    """
    Dependencia para obtener una sesión de base de datos.
    Se usa en las rutas para manejar la conexión de manera segura.
    """
    db = SessionLocal()
    try:
        yield db  # Entrega la sesión al contexto de ejecución
    finally:
        db.close()  # Cierra la sesión al finalizar
