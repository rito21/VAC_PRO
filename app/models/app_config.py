from sqlalchemy import Column, Integer, String
from app.services.database import Base


class AppConfig(Base):
    __tablename__ = "app_config"

    id = Column(Integer, primary_key=True, index=True)
    smtp_server = Column(String(255), nullable=False)
    smtp_user = Column(String(255), nullable=False)
    smtp_password = Column(String, nullable=False)  # Cambié "text" a String