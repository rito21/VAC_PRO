from fastapi import Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuari import Usuari as UsuariModel  # Modelo SQLAlchemy
from app.schemas.usuari import Usuari as UsuariSchema  # Esquema Pydantic
from decouple import config
import bcrypt
from sqlalchemy.sql import func  # Añadido para usar func.now() si es necesario

# Configuración de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Configuración de JWT con valores predeterminados
SECRET_KEY = config("SECRET_KEY", default="your-default-secret-key-12345")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_SECONDS = config("ACCESS_TOKEN_EXPIRE_SECONDS", default=3600, cast=int)

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(UsuariModel).filter(UsuariModel.correu_electronic == email).first()
    return user if user and verify_password(password, user.contrasenya) else None

async def get_current_user(token: str = Cookie(None), db: Session = Depends(get_db)):
    """Obtiene el usuario autenticado mediante cookie JWT"""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = verify_token(token)
    email = payload.get("sub")

    user = db.query(UsuariModel).filter(UsuariModel.correu_electronic == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user.bloquejat:
        raise HTTPException(status_code=403, detail="User is blocked")

    return UsuariSchema.model_validate(user)  # Conversión SQLAlchemy → Pydantic

async def get_current_user_no_db(token: str = Cookie(None)):
    """Obtiene el usuario actual a partir del token sin acceder a la base de datos."""
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = verify_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    # Creamos un objeto Usuari básico con los datos del token
    user = UsuariSchema(correu_electronic=email)
    return user