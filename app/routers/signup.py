from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request, status, Form, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.auth import login
from app.dependencies import get_db
from app.email_verificator import send_verification_email
from app.models.usuari import Usuari
from app.services.services_usuari import create_user

router = APIRouter(prefix='/signup', tags=['signup'])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def signup(request: Request):
    return templates.TemplateResponse("register/signup.html", {"request": request})


@router.post("/")
def signup(request: Request,
           correu_electronic: str = Form(...),
           contrasenya: str = Form(...),
           nom_complet: str = Form(...),
           db: Session = Depends(get_db)):
    # Verificar si l'usuari ja existeix
    db_user = db.query(Usuari).filter(Usuari.correu_electronic == correu_electronic).first()
    # TODO: enviar a login.html?
    if db_user:
        return templates.TemplateResponse("signup.html", {
            "request": request,
            "error_message": "Correu electrònic ja registrat"
        })

    # Validar la força de la contrasenya
    if not login.is_valid_password(contrasenya):
        return templates.TemplateResponse("/register/signup.html", {
            "request": request,
            "error_message": "La contrasenya no compleix els requisits de seguretat! "
                             "Ha de tenir almenys 8 caràcters\n"
                                "Ha de contenir almenys un dígit\n" 
                                "Ha de contenir almenys una lletra\n"   
                                "Ha de contenir almenys un caràcter especial -> !@#$%^&*(),.?"
        })

    new_user = Usuari(
        correu_electronic=correu_electronic,
        contrasenya=contrasenya,
        nom_complet=nom_complet,
        data_creacio=datetime.now(timezone.utc),
    )

    acces_token = login.create_access_token(user=new_user)
    send_verification_email(email=correu_electronic, token=acces_token)
    create_user(db, new_user)

    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get('/verify/{token}')
def verify_user(token: str, db: Session = Depends(get_db)):
    payload = login.verify_token(token)
    username = payload.get("correu_electronic")
    db_user = db.query(Usuari).filter(Usuari.correu_electronic == username).first()

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credencials no correctes"
        )

    if db_user.es_actiu:
        return "El teu compte ja està activat !"

    db_user.is_active = True
    db.commit()
    response = RedirectResponse(url="/signup")
    return response
