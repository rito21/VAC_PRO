from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from starlette import status
from starlette.responses import JSONResponse

from app.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)


async def send_verification_email(email: EmailStr, token: str) -> JSONResponse:
    # Provar si pot possar-se un botó
    html_button = f"""<form method="post">
                        <a class="signin__link"  href="http://localhost:8080/signup/verify/{token}">verify account</a>      
                     </form>"""
    message = MessageSchema(
        subject="Verificació de correu electrònic",
        recipients=[email],  # Llista de correus electrònics
        body=f"Segueix aquest enllaç per verificar el teu compte: http://localhost:8000/signup/verify?token={token}<BR><BR>"
             f"{html_button}",
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "email has been sent"})
