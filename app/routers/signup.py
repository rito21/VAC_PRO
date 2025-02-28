from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Request, status, Form, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from app.auth.login import hash_password, is_valid_password, create_access_token, verify_token
from app.database import get_db
from app.email_verificator import send_verification_email
from app.services.crud import create_user
from app.models.usuari import Usuari
from app.models.config import TblConfig
from app.schemas.usuari import UsuariCreate

router = APIRouter(prefix='/signup', tags=['signup'])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def signup(request: Request):
    return templates.TemplateResponse("register/signup.html", {"request": request})

@router.post("/")
async def signup(
    request: Request,
    correu_electronic: str = Form(...),
    contrasenya: str = Form(...),
    confirmar_contrasenya: str = Form(...),
    nom: str = Form(...),
    cognoms: str = Form(...),
    acceptar_privacitat: bool = Form(...),
    promocions: bool = Form(False),
    db: Session = Depends(get_db)
):
    print("Iniciando registro para:", correu_electronic)
    # Verificar si las contraseñas coinciden
    if contrasenya != confirmar_contrasenya:
        print("Error: Contraseñas no coinciden")
        return templates.TemplateResponse("register/signup.html", {
            "request": request,
            "error_message": "Les contrasenyes no coincideixen"
        })

    # Verificar si el usuario ya existe
    print("Verificando si el usuario existe...")
    db_user = db.query(Usuari).filter(Usuari.correu_electronic == correu_electronic).first()
    if db_user:
        print("Error: Correu electrònic ya registrado")
        return templates.TemplateResponse("register/signup.html", {
            "request": request,
            "error_message": "Correu electrònic ja registrat"
        })

    # Obtener la configuración de la empresa
    print("Obteniendo configuración de la empresa...")
    config = db.query(TblConfig).filter(TblConfig.empresa == 1).first()
    if not config:
        print("Error: Configuración de la empresa no encontrada")
        raise HTTPException(status_code=500, detail="Configuració de l'empresa no trobada")

    # Validar la contraseña
    print("Validando contraseña...")
    if len(contrasenya) < config.longitud_minima_contrasenya or not is_valid_password(contrasenya, db):
        print("Error: Contraseña no válida")
        return templates.TemplateResponse("register/signup.html", {
            "request": request,
            "error_message": f"La contrasenya ha de tenir almenys {config.longitud_minima_contrasenya} caràcters\n"
                             "Ha de contenir almenys un dígit\n"
                             "Ha de contenir almenys una lletra\n"
                             "Ha de contenir almenys un caràcter especial -> !@#$%^&*(),.?"
        })

    # Crear el usuario
    print("Creando datos del usuario...")
    user_data = UsuariCreate(
        correu_electronic=correu_electronic,
        contrasenya=contrasenya,
        nom=nom,
        cognoms=cognoms,
        id_empresa=1
    )
    new_user = Usuari(
        correu_electronic=user_data.correu_electronic,
        contrasenya=hash_password(user_data.contrasenya),
        nom=user_data.nom,
        cognoms=user_data.cognoms,
        id_empresa=user_data.id_empresa,
        data_registre=datetime.now(timezone.utc),
    )

    # Guardar el usuario y enviar email de verificación
    print("Guardando usuario en la base de datos...")
    create_user(db, new_user)
    print("Generando token de acceso...")
    access_token = create_access_token(new_user)
    print("Enviando correo de verificación...")
    await send_verification_email(email=correu_electronic, token=access_token)

    # Mostrar página de confirmación
    print("Mostrando página de confirmación...")
    return templates.TemplateResponse("register/confirmation.html", {
        "request": request,
        "message": "S'ha enviat un correu de verificació al teu correu electrònic."
    })

@router.get('/verify/{token}')
def verify_user(token: str, db: Session = Depends(get_db)):
    payload = verify_token(token)
    username = payload.get("correu_electronic")
    db_user = db.query(Usuari).filter(Usuari.correu_electronic == username).first()

    if not username or not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credencials no correctes"
        )

    if db_user.compte_verificat:
        return "El teu compte ja està activat!"

    db_user.compte_verificat = True
    db.commit()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)