from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/index', tags=['index'])

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def index(request: Request):
    """
    Gestiona la ruta de la página de inicio.
    """
    return templates.TemplateResponse("index.html", {"request": request})