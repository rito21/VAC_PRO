from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.login import authenticate_user, create_access_token
from app.models.usuari import Usuari

router = APIRouter(prefix='/login', tags=['login'])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def login_page(request: Request):
    """Muestra la página de login."""
    return templates.TemplateResponse("register/login.html", {"request": request})

@router.post("/")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Autentica al usuario y almacena el token en cookies seguras."""
    user = authenticate_user(email, password, db)

    if not user:
        return templates.TemplateResponse("register/login.html", {
            "request": request,
            "error_message": "⚠️ Correu electrònic o contrasenya incorrectes"
        }, status_code=400)  # ⛔ Devuelve error 400

    access_token = create_access_token(data={"sub": user.correu_electronic})

    response = RedirectResponse(url="/dashboard/", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # 🔒 Solo HTTPS
        samesite="Lax"
    )
    return response

@router.get("/logout")
async def logout(request: Request):
    """Elimina la cookie de sesión y redirige a la página principal."""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response
