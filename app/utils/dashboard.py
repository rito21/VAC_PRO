from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.models.usuari import Usuari
from app.models.device import Device
from app.database import get_db

templates = Jinja2Templates(directory="templates")

def render_dashboard(request: Request, user: Usuari) -> dict:
    """Renderiza la plantilla del dashboard."""
    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "user": user})

def render_register_device_page(request: Request, user: Usuari, success_message: str = None) -> dict:
    """Renderiza la página para registrar un dispositivo."""
    return templates.TemplateResponse("dashboard/register_device.html", {
        "request": request,
        "user": user,
        "success_message": success_message
    })

def register_device(request: Request, user: Usuari, name: str, latitude: float, longitude: float, db: Session) -> dict:
    """Registra un nuevo dispositivo en la base de datos y renderiza la página con un mensaje de éxito."""
    device = Device(
        user_id=user.id,
        name=name,
        latitude=latitude,
        longitude=longitude
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return render_register_device_page(request, user, success_message=f"Dispositiu '{name}' registrat amb èxit!")

def render_device_data_page(request: Request, user: Usuari) -> dict:
    """Renderiza la página de datos de dispositivos."""
    return templates.TemplateResponse("dashboard/device_data.html", {"request": request, "user": user})

def render_device_map_page(request: Request, user: Usuari) -> dict:
    """Renderiza la página del mapa de dispositivos."""
    return templates.TemplateResponse("dashboard/device_map.html", {"request": request, "user": user})