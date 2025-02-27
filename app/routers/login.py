from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from app.database import get_db
from app.auth.login import create_access_token, verify_password, authenticate_user

router = APIRouter(prefix="/login", tags=["login"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def login_page(request: Request):
    return templates.TemplateResponse("register/login.html", {"request": request})

@router.post("/")
def login(
    request: Request,
    correu_electronic: str = Form(...),
    contrasenya: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(correu_electronic, contrasenya, db)
    access_token = create_access_token(user)
    # Aquí puedes manejar el token como desees, por ejemplo, almacenarlo en una cookie o redirigir
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)