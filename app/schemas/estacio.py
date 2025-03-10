from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

from app.schemas.sensor import SensorInDB

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

class EstacioMeteoInDB(EstacioMeteoBase):
    id: int
    data_creacio: datetime
    ultima_connexio: Optional[datetime] = None
    sensors: List[SensorInDB] = []

    model_config = ConfigDict(from_attributes=True) 