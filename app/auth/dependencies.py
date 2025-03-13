from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.login import verify_token
from app.models.usuari import Usuari
from app.schemas.usuari import UsuariResponse
from typing import Optional

async def get_authenticated_user(request: Request, db: Session = Depends(get_db)) -> Optional[UsuariResponse]:
    token = request.cookies.get("access_token")
    if not token:
        return None

    payload = verify_token(token)
    if not payload:
        return None

    user = db.query(Usuari).filter(Usuari.correu_electronic == payload.get("sub")).first()
    if not user:
        return None

    return UsuariResponse.model_validate(user)
