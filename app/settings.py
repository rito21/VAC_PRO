import urllib
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    load_dotenv()  # Carrega variables d'entorn des del fitxer .env

    # Configuració de la base de dades
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_DBNAME: str
    DATABASE_SSL_MODE: str

    # Configuració de seguretat
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int

    # Configuració de correu electrònic
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool

    # Altres configuracions
    DEFAULT_MIN_PASSWORD_LENGTH: int  # Ara es pot configurar per empresa a tbl_config
    MAX_LOGIN_ATTEMPTS: int  # També configurable per empresa
    TESTING: bool = False

    @property
    def get_database_url(self):
        """
        Retorna l'URL de la base de dades.
        Si està en mode TESTING, retorna una base de dades SQLite.
        """
        if self.TESTING:
            return "sqlite:///./test.db"  # Base de dades de test
        return self.database_url

    class Config:
        env_file = ".env"  # Indica el fitxer d'entorn


settings = Settings()

# Constants de seguretat
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_SECONDS = settings.ACCESS_TOKEN_EXPIRE_SECONDS
COOKIE_NAME = "access_token"

# Codifica la contrasenya per evitar errors amb caràcters especials (@, #, $, etc.)
settings.DATABASE_PASSWORD = urllib.parse.quote_plus(settings.DATABASE_PASSWORD)

# URI per SQLAlchemy amb PostgreSQL i psycopg2
SQLALCHEMY_DATABASE_URI: str = (
    f"postgresql+psycopg2://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}"
    f"@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_DBNAME}"
    f"?sslmode={settings.DATABASE_SSL_MODE}"
)
