from pydantic import BaseModel

class App_Config(BaseModel):
    smtp_server: str
    smtp_user: str
    smtp_password: str
    id: int

    model_config = {"from_attributes": True}  # Pydantic v2