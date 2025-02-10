from fastapi.security import OAuth2PasswordBearer

from app.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_db():
    """
    Obté una connexió a la base de dades des del pool de sessions local.
    Retorna:
        Un objecte de connexió a la base de dades.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
