from pydantic import BaseModel

class AppConfigBase(BaseModel):
    smtp_server: str
    smtp_user: str
    smtp_password: str

class AppConfigInDB(AppConfigBase):
    id: int

    class Config:
        orm_mode = True
