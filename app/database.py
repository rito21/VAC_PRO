from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@" \
                          f"{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_DBNAME}" \
                          f"?sslmode={settings.DATABASE_SSL_MODE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
