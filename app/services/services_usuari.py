from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status
from werkzeug.security import generate_password_hash

from app.models.usuari import Usuari
from app.schemas.usuari import UsuariCreate


def create_user(db: Session, user: UsuariCreate):
    try:
        hashed_password = generate_password_hash(user.contrasenya)  # Encriptació de la contrasenya
        db_user = Usuari(correu_electronic=user.correu_electronic, contrasenya=hashed_password, nom_complet=user.nom_complet)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error en la creació de l'usuari: {e}")


def get_user_by_email(db: Session, email: EmailStr):
    user = db.query(Usuari).filter(Usuari.correu_electronic == email).first()
    return user
