from decouple import config

class Settings:
    # Base de datos (ya manejada en database.py, pero aquí para referencia)
    DATABASE_USER = config("DATABASE_USER")
    DATABASE_PASSWORD = config("DATABASE_PASSWORD")
    DATABASE_HOST = config("DATABASE_HOST")
    DATABASE_PORT = config("DATABASE_PORT", cast=int)
    DATABASE_DBNAME = config("DATABASE_DBNAME")
    DATABASE_SSL_MODE = config("DATABASE_SSL_MODE")

    # Seguridad y autenticación
    SECRET_KEY = config("SECRET_KEY")
    ALGORITHM = config("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_SECONDS = config("ACCESS_TOKEN_EXPIRE_SECONDS", cast=int)  # Asegúrate de que coincida con .env
    DEFAULT_MIN_PASSWORD_LENGTH = config("DEFAULT_MIN_PASSWORD_LENGTH", cast=int)
    MAX_LOGIN_ATTEMPTS = config("MAX_LOGIN_ATTEMPTS", cast=int)

    # Configuración del correo
    MAIL_USERNAME = config("MAIL_USERNAME")
    MAIL_PASSWORD = config("MAIL_PASSWORD")
    MAIL_FROM = config("MAIL_FROM")
    MAIL_PORT = config("MAIL_PORT", cast=int)
    MAIL_SERVER = config("MAIL_SERVER")
    MAIL_FROM_NAME = config("MAIL_FROM_NAME")
    MAIL_STARTTLS = config("MAIL_STARTTLS", cast=bool)
    MAIL_SSL_TLS = config("MAIL_SSL_TLS", cast=bool)
    USE_CREDENTIALS = config("USE_CREDENTIALS", cast=bool)
    VALIDATE_CERTS = config("VALIDATE_CERTS", cast=bool)

settings = Settings()