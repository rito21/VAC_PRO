from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

router = APIRouter(prefix="/politica-privacitat", tags=["politica-privacitat"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def politica_privacitat(request: Request):
    return templates.TemplateResponse("register/politica-privacitat.html", {"request": request})