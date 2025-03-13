from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EstacioMeteoBase(BaseModel):
    nom: str
    descripcio: Optional[str] = None
    ubicacio: Optional[str] = None
    id_empresa: int
    estat: bool = True
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    versio_firmware: Optional[str] = None

class EstacioMeteoCreate(EstacioMeteoBase):
    pass

class EstacioMeteo(EstacioMeteoBase):
    id: int
    data_creacio: datetime
    ultima_connexio: Optional[datetime] = None

    class Config:
        from_attributes = True 