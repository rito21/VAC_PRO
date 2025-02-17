from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuariBase(BaseModel):
    nom: str
    cognoms: str
    correu: EmailStr

class UsuariCreate(UsuariBase):
    contrasenya: str  # Al recibir datos, no almacenamos contraseñas directamente, solo el hash

class UsuariUpdate(UsuariBase):
    contrasenya: Optional[str] = None  # Solo actualizamos la contraseña si se envía

class UsuariInDB(UsuariBase):
    id: int
    data_registre: datetime
    ultim_canvi_contrasenya: datetime
    intents_fallits_login: int
    bloquejat: bool
    baixa: bool
    compte_verificat: bool

    class Config:
        orm_mode = True  # Para que pueda interactuar con los modelos de SQLAlchemy
