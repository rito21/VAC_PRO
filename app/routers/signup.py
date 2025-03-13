from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.login import get_password_hash, verify_password, create_access_token, verify_token
from app.models.usuari import Usuari
import re
from datetime import timedelta

router = APIRouter(prefix='/signup', tags=['signup'])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def signup_page(request: Request):
    return templates.TemplateResponse("register/signup.html", {"request": request})

@router.post("/")
async def signup(
    request: Request,
    nom: str = Form(...),
    cognoms: str = Form(...),
    correu_electronic: str = Form(...),
    contrasenya: str = Form(...),
    confirmar_contrasenya: str = Form(...),
    acceptar_privacitat: bool = Form(False),
    promocions: bool = Form(False),
    db: Session = Depends(get_db)
):
    # Validar que las contraseñas coincidan
    if contrasenya != confirmar_contrasenya:
        return templates.TemplateResponse("register/signup.html", {
            "request": request,
            "error_message": "Les contrasenyes no coincideixen",
            "nom": nom,
            "cognoms": cognoms,
            "correu_electronic": correu_electronic
        })

    # Validar la contraseña (mínimo 8 caracteres, 1 mayúscula, 1 número, 1 símbolo)
    if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$", contrasenya):
        return templates.TemplateResponse("register/signup.html", {
            "request": request,
            "error_message": "La contrasenya ha de tenir almenys 8 caràcters, incloure 1 majúscula, 1 número i 1 símbol (!@#$%^&*)",
            "nom": nom,
            "cognoms": cognoms,
            "correu_electronic": correu_electronic
        })

    # Validar que se haya aceptado la política de privacidad
    if not acceptar_privacitat:
        return templates.TemplateResponse("register/signup.html", {
            "request": request,
            "error_message": "Has d'acceptar la política de privacitat",
            "nom": nom,
            "cognoms": cognoms,
            "correu_electronic": correu_electronic
        })

    # Verificar si el correo ya está registrado
    existing_user = db.query(Usuari).filter(Usuari.correu_electronic == correu_electronic).first()
    if existing_user:
        return templates.TemplateResponse("register/signup.html", {
            "request": request,
            "error_message": "Aquest correu electrònic ja està registrat",
            "nom": nom,
            "cognoms": cognoms,
            "correu_electronic": correu_electronic
        })

    # Crear un nuevo usuario
    hashed_password = get_password_hash(contrasenya)
    new_user = Usuari(
        id_empresa=1,  # Asumimos que todos los usuarios pertenecen a la empresa con id=1
        nom=nom,
        cognoms=cognoms,
        correu_electronic=correu_electronic,
        contrasenya=hashed_password,
        bloquejat=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generar token de verificación
    verification_token = create_access_token(data={"sub": correu_electronic, "bloquejat": False}, expires_delta=timedelta(minutes=30))

    # En un entorno real, enviaríamos un correo electrónico con el enlace de verificación
    # Por ahora, simulamos el enlace
    verification_url = f"{request.base_url}signup/verify/{verification_token}"

    return templates.TemplateResponse("register/signup.html", {
        "request": request,
        "success_message": f"Registre completat! Revisa el teu correu electrònic per verificar el teu compte. Enlace de verificación: {verification_url}",
        "nom": nom,
        "cognoms": cognoms,
        "correu_electronic": correu_electronic
    })

@router.get("/verify/{token}", response_model=None)
async def verify_user(token: str, request: Request, db: Session = Depends(get_db)):
    payload = verify_token(token)
    email = payload.get("sub")
    if email is None:
        return templates.TemplateResponse("register/verify.html", {
            "request": request,
            "error_message": "Enllaç de verificació invàlid"
        })

    user = db.query(Usuari).filter(Usuari.correu_electronic == email).first()
    if not user:
        return templates.TemplateResponse("register/verify.html", {
            "request": request,
            "error_message": "Usuari no trobat"
        })

    if user.compte_verificat:
        return templates.TemplateResponse("register/verify.html", {
            "request": request,
            "success_message": "El teu compte ja està verificat. Pots iniciar sessió."
        })

    user.compte_verificat = True
    db.commit()
    db.refresh(user)

    return templates.TemplateResponse("register/verify.html", {
        "request": request,
        "success_message": "Compte verificat amb èxit! Ja pots iniciar sessió."
    })