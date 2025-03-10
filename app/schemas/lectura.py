from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class LecturaBase(BaseModel):
    id_sensor: int
    valor: float
    data_lectura: datetime
    qualitat_lectura: Optional[int] = Field(None, ge=0, le=100)
    bateria: Optional[float] = None
    rssi: Optional[int] = None
    metadata: Optional[dict] = None

class LecturaCreate(LecturaBase):
    pass

class LecturaInDB(LecturaBase):
    id: int

    model_config = ConfigDict(from_attributes=True) 