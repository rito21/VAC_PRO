from pydantic import BaseModel


class Token(BaseModel):
    access_token: str  # El token de acceso generado para el usuario
    token_type: str = "bearer"  # El tipo de token, por lo general es "bearer"
