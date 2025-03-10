from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

from app.schemas.lectura import LecturaInDB

class TipusSensorBase(BaseModel):
    nom: str
    descripcio: Optional[str] = None
    unitat: str

class TipusSensorCreate(TipusSensorBase):
    pass

class TipusSensorInDB(TipusSensorBase):
    id: int
    data_creacio: datetime

    model_config = ConfigDict(from_attributes=True)

class SensorBase(BaseModel):
    nom: str
    id_estacio: int
    id_tipus_sensor: int
    estat: bool = True
    calibracio: Optional[dict] = None

class SensorCreate(SensorBase):
    pass

class SensorInDB(SensorBase):
    id: int
    data_creacio: datetime
    ultima_lectura: Optional[datetime] = None
    lectures: List[LecturaInDB] = []

    model_config = ConfigDict(from_attributes=True) 