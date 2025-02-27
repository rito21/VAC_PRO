# app/models/app_config.py
from sqlalchemy import Column, Integer, String
from app.database import Base  # La base para todos los modelos

class AppConfig(Base):
    __tablename__ = 'app_config'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)

