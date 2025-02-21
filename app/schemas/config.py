from pydantic import BaseModel
from datetime import datetime

class ConfigBase(BaseModel):
    longitud_minima_contrasenya: int = 8
    intents_fallits_maxims: int = 5

class ConfigInDB(ConfigBase):
    id: int
    empresa_id: int
    data_ultim_canvi_contrasenya: datetime

    class Config:
        from_attributes = True
