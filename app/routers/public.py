from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/serveis")
async def serveis(request: Request):
    return templates.TemplateResponse("serveis.html", {"request": request})

@router.get("/contacte/")
async def contacte(request: Request):
    return templates.TemplateResponse("contacte.html", {"request": request})
# Ruta para la página de política de privacidad


@router.get("/")
async def nueva_politica_privacidad(request: Request):
    return templates.TemplateResponse("register/nueva_politica_privacidad.html", {"request": request})
