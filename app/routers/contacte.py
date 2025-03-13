from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/contacte/")
async def contacte(request: Request):
    return templates.TemplateResponse("contacte.html", {"request": request})