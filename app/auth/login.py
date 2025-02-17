import re
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import HTTPException, Depends, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from app.dependencies import get_db
from app.settings import ACCESS_TOKEN_EXPIRE_SECONDS, SECRET_KEY, ALGORITHM, settings
from app.models.usuari import DbUsuari


def authenticate_user(email: str, password: str, db: Session):
    """
    Autentica un usuari basant-se en el seu correu electrònic i contrasenya.
     Paràmetres:
        email (str): El correu electrònic de l'usuari.
        password (str): La contrasenya de l'usuari.
        db (Session): L'objecte de sessió de la base de dades.
     Retorna:
        user: L'objecte d'usuari autenticat.
     Llença:
        HTTPException: Si no es troba l'usuari, el compte està bloquejat per intents d'inici de sessió excessius o la contrasenya és incorrecta.
    """
    user = db.query(DbUsuari).filter(DbUsuari.correu == email).first()
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


def is_valid_password(password: str):
    """
    Comprova si una contrasenya és vàlida basant-se en els següents criteris:
    - Ha de tenir almenys 8 caràcters.
    - Ha de contenir almenys un dígit.
    - Ha de contenir almenys una lletra.
    - Ha de contenir almenys un caràcter especial.

    Retorna:
        bool: True si la contrasenya és vàlida, False en cas contrari.
    """
    if len(password) < settings.DEFAULT_MIN_PASSWORD_LENGTH:
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search("[a-zA-Z]", password):
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True


def verify_password(plain_password, hashed_password):
    """
    Verifica si una contrasenya en clar coincideix amb una contrasenya hashada donada.
    """
    return check_password_hash(hashed_password, plain_password)


def create_access_token(user: DbUsuari):
    """
    Crea un token d'accés per a un usuari donat.
    """
    try:
        expire = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
        payload = {
            "correu": user.correu,
            "bloquejat": user.bloquejat,
            "expire": expire.strftime("%Y-%m-%d %H:%M:%S")
        }
        return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex


def verify_token(token: str) -> bool:
    """
    Verifica si un token és vàlid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("correu")
        if username is None:
            return False
        return True
    except JWTError:
        return False


def get_current_user(token: str, db: Session = Depends(get_db)):
    """
    Obté l'usuari actual basant-se en el token d'accés proporcionat.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No s'han pogut validar les credencials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not verify_token(token):
        raise credentials_exception
    username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("correu")
    user = db.query(DbUsuari).filter(DbUsuari.correu == username).first()
    if user is None:
        raise credentials_exception
    return user
