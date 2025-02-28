import re
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import HTTPException, Depends, status
from passlib.context import CryptContext
import jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.settings import settings  # Importamos solo la instancia settings
from app.models.usuari import Usuari
from app.models.config import TblConfig

# Configuración de passlib para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con una hasheada."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str, db: Session) -> Usuari:
    """
    Autentica un usuario basándose en su correo electrónico y contraseña.
    """
    user = db.query(Usuari).filter(Usuari.correu_electronic == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuari no trobat")
    if user.intents_fallits_login >= 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Compte bloquejat per intents excessius")
    if not verify_password(password, user.contrasenya):
        user.intents_fallits_login += 1
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contrasenya incorrecta")
    user.intents_fallits_login = 0
    db.commit()
    return user


def is_valid_password(password: str, db: Session) -> bool:
    """
    Comprueba si una contraseña es válida según los criterios de la empresa (tbl_config).
    """
    config = db.query(TblConfig).filter(TblConfig.empresa == 1).first()
    if not config:
        raise HTTPException(status_code=500, detail="Configuració de l'empresa no trobada")

    if len(password) < config.longitud_minima_contrasenya:
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search("[a-zA-Z]", password):
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


def create_access_token(user: Usuari) -> str:
    """
    Crea un token de acceso para un usuario dado.
    """
    try:
        expire = datetime.now(timezone.utc) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        payload = {
            "correu_electronic": user.correu_electronic,
            "bloquejat": user.bloquejat,
            "exp": expire
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex


def verify_token(token: str) -> Optional[dict]:
    """
    Verifica si un token es válido y devuelve su payload.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("correu_electronic") is None:
            return None
        return payload
    except jwt.JWTError:
        return None


def get_current_user(token: str, db: Session = Depends(get_db)) -> Usuari:
    """
    Obtiene el usuario actual basado en el token de acceso proporcionado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No s'han pogut validar les credencials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    if not payload:
        raise credentials_exception
    username = payload.get("correu_electronic")
    user = db.query(Usuari).filter(Usuari.correu_electronic == username).first()
    if user is None:
        raise credentials_exception
    return user