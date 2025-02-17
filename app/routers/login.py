from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.auth.login import create_access_token, verify_password
from app.settings import ACCESS_TOKEN_EXPIRE_SECONDS, COOKIE_NAME
from app.dependencies import get_db
from app.schemas.token import Token
from app.services.services_usuari import get_user_by_email

router = APIRouter(prefix='/login', tags=['login'])

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def login(request: Request):
    """
    Gestiona la ruta de login. Aquesta pàgina inclou el formulari d'inici de sessió.
    """
    return templates.TemplateResponse("register/login.html", {"request": request})


@router.post("/", response_model=Token)
def login_for_access_token(request: Request,
                            db: Session = Depends(get_db),
                            form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Gestiona la petició de login i retorna un token d'accés si les dades són correctes.
    :param request: Petició HTTP
    :param db: sessió de la base de dades
    :param form_data: dades del formulari d'inici de sessió
    :return: petició de redirecció amb el token d'accés
    """
    # Obtenir usuari per correu electrònic
    user = get_user_by_email(db, email=form_data.username)

    # Comprovar si l'usuari existeix i si la contrasenya és correcta
    if not user or not verify_password(form_data.password, user.contrasenya):
        return templates.TemplateResponse(name="login.html",
                                          context={"request": request,
                                                   "error_message": "Correu electrònic o contrasenya incorrectes"},
                                          status_code=status.HTTP_401_UNAUTHORIZED
                                          )

    # Crear el token d'accés
    access_token = create_access_token(user)

    # Redirigir a la pàgina principal amb el token com a cookie
    return RedirectResponse("/",
                            status_code=status.HTTP_302_FOUND,
                            headers={
                                "set-cookie": f"{COOKIE_NAME}={access_token}; Max-Age={ACCESS_TOKEN_EXPIRE_SECONDS}; Path=/"
                            })
