from pydantic import BaseModel, EmailStr, constr


class UsuariCreate(BaseModel):
    correu_electronic: EmailStr
    contrasenya: constr(min_length=8)
    nom_complet: str


class UsuariLogin(BaseModel):
    correu_electronic: EmailStr
    contrasenya: str
    nom_complet: str


class UsuariInfo(BaseModel):
    id: int
    correu_electronic: EmailStr
    es_actiu: bool
    es_admin: bool
    nom_complet: str

    class ConfigDict:
        from_attributes = True
