from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UsuariBase(BaseModel):
    correu_electronic: EmailStr
    nom: str
    cognoms: str

class UsuariCreate(UsuariBase):
    contrasenya: str
    id_empresa: int = 1  # Valor por defecto para empresa única

class Usuari(UsuariBase):
    id: int
    id_empresa: int
    data_registre: datetime
    ultim_canvi_contrasenya: datetime
    intents_fallits_login: int
    bloquejat: bool
    baixa: bool
    compte_verificat: bool

    model_config = ConfigDict(from_attributes=True)  # ✅ Corrección para Pydantic v2
