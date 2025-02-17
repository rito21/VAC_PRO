from fastapi.security import OAuth2PasswordBearer
from app.database import SessionLocal  # Asegúrate de que SessionLocal esté configurado correctamente

# Define el esquema de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    """
    Obté una connexió a la base de dades des del pool de sessions local.
    Retorna:
        Un objecte de connexió a la base de dades.
    """
    db = SessionLocal()  # Obtiene una sesión de la base de datos
    try:
        yield db  # Devuelve la sesión para ser utilizada en las dependencias
    finally:
        db.close()  # Asegura que la sesión se cierra después de su uso
