# app/schemas/app_config.py
from pydantic import BaseModel

class AppConfigBase(BaseModel):
    key: str
    value: str

class AppConfigCreate(AppConfigBase):
    pass

class AppConfig(AppConfigBase):
    id: int

    class Config:
        orm_mode = True
