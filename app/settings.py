# import urllib
#
# from dotenv import load_dotenv
# from pydantic_settings import BaseSettings
#
#
# class Settings(BaseSettings):
#     load_dotenv()  # Així funciona tant als tests com a l'aplicació
#     DATABASE_USER: str
#     DATABASE_PASSWORD: str
#     DATABASE_HOST: str
#     DATABASE_PORT: int
#     DATABASE_DBNAME: str
#     DATABASE_SSL_MODE: str
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_SECONDS: int
#     MAIL_USERNAME: str
#     MAIL_PASSWORD: str
#     MAIL_FROM: str
#     MAIL_PORT: int
#     MAIL_SERVER: str
#     MAIL_FROM_NAME: str
#     MAIL_STARTTLS: bool
#     MAIL_SSL_TLS: bool
#     USE_CREDENTIALS: bool
#     VALIDATE_CERTS: bool
#     DEFAULT_MIN_PASSWORD_LENGTH: int
#     TESTING: bool = False
#
#     # @property
#     def get_database_url(self):
#         if self.TESTING:
#             return "sqlite:///./test.db"  # Base de dades per a tests
#         return self.DATABASE_URL
#
#     class Config:
#         env_file = '.env'
#
#
# settings = Settings()
#
# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM
# ACCESS_TOKEN_EXPIRE_SECONDS = settings.ACCESS_TOKEN_EXPIRE_SECONDS
# COOKIE_NAME = 'access_token'
#
# # Adaptem la contrasenya per si té caràcters especials @#$%....
# settings.DATABASE_PASSWORD = urllib.parse.quote_plus(settings.DATABASE_PASSWORD)
#
# # SQL Alchemy
# SQLALCHEMY_DATABASE_URI: str = f"DATABASEql+psycopg2://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_DBNAME}?sslmode={settings.DATABASE_SSL_MODE}"
