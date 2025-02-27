from sqlalchemy.orm import Session
from app.models.usuari import Usuari

def create_user(db: Session, user: Usuari):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user