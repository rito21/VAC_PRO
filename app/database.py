from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"  # Ajusta según tu base de datos

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """Inicializa la base de datos con una empresa predeterminada y su configuración."""
    from app.models.empresa import DbEmpresa
    from app.models.usuari import Usuari
    from app.models.config import TblConfig

    # Verificamos si las tablas ya existen usando inspect
    inspector = inspect(engine)
    tables_exist = inspector.has_table("db_empresa")

    # Creamos las tablas solo si no existen
    if not tables_exist:
        Base.metadata.create_all(bind=engine)

    # Ahora abrimos la sesión para inicializar datos
    with SessionLocal() as db:
        if not db.query(DbEmpresa).filter(DbEmpresa.id == 1).first():
            empresa = DbEmpresa(id=1, nom_empresa="Empresa Única")
            db.add(empresa)
            db.commit()
            db.refresh(empresa)
            config = TblConfig(
                empresa=1,
                longitud_minima_contrasenya=8,
                intents_fallits_maxims=5
            )
            db.add(config)
            db.commit()


def get_db():
    """Dependencia para obtener una sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Llamamos a init_db solo una vez al importar el módulo
init_db()