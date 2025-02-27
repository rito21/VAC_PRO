from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/politica-privacitat", tags=["politica-privacitat"])

templates = Jinja2Templates(directory="templates")


@router.get("/", name="politica_privacitat")
async def politica_privacitat(request: Request):
    """
    Gestiona la ruta de la política de privacitat. Renderitza la plantilla corresponent.
    :param request: Petició HTTP
    :return: Resposta amb la plantilla renderitzada
    """
    return templates.TemplateResponse("politica-privacitat.html", {"request": request})