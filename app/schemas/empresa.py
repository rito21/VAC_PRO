from pydantic import BaseModel
from typing import List

from app.schemas.usuari import UsuariInDB


class EmpresaBase(BaseModel):
    nom_empresa: str

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaInDB(EmpresaBase):
    id: int
    usuaris: List[UsuariInDB]  # Relación con usuarios, si es necesario

    class Config:
        from_attributes = True
