from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AppConfig(Base):
    __tablename__ = 'app_config'

    id = Column(Integer, primary_key=True, index=True)
    smtp_server = Column(String(255), nullable=False)
    smtp_user = Column(String(255), nullable=False)
    smtp_password = Column(Text, nullable=False)
