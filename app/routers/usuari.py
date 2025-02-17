from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.services.services_usuari as crud
from app.dependencies import get_db
from app.schemas.usuari import UsuariCreate, UsuariInDB

router = APIRouter(prefix="/usuari", tags=["usuari"])

@router.post("/", response_model=UsuariInDB, status_code=status.HTTP_201_CREATED)
def create_user(user: UsuariCreate, db: Session = Depends(get_db)):
    """
    Crea un nou usuari.
    :param user: Dades de l'usuari a crear.
    :param db: Sessió de la base de dades.
    :return: L'usuari creat.
    """
    db_user = crud.get_user_by_email(db, email=user.correu_electronic)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Correu electrònic ja registrat")
    return crud.create_user(db=db, user=user)

@router.put("/{user_id}", response_model=UsuariInDB)
def update_user(user_id: int, user: UsuariCreate, db: Session = Depends(get_db)):
    """
    Actualitza les dades d'un usuari existent.
    :param user_id: ID de l'usuari a actualitzar.
    :param user: Noves dades de l'usuari.
    :param db: Sessió de la base de dades.
    :return: Usuari actualitzat.
    """
    updated_user = crud.update_user(db=db, user_id=user_id, user=user)
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuari no trobat")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Elimina un usuari.
    :param user_id: ID de l'usuari a eliminar.
    :param db: Sessió de la base de dades.
    :return: Missatge de confirmació de l'eliminació.
    """
    success = crud.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuari no trobat")
    return {"message": "Usuari eliminat"}
