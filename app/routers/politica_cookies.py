from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/politica-cookies/")
async def politica_cookies(request: Request):
    return templates.TemplateResponse("politica_cookies.html", {"request": request})