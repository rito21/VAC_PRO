from fastapi.responses import HTMLResponse
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.estacio_meteo import EstacioMeteo
from app.schemas.estacio_meteo import EstacioMeteoCreate
from app.auth.login import get_current_user

templates = Jinja2Templates(directory="templates")

def render_dashboard(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    devices = db.query(EstacioMeteo).filter(EstacioMeteo.id_empresa == current_user.id_empresa).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "devices": devices, "current_user": current_user}
    )

def render_register_device_page(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "register_device.html",
        {"request": request, "current_user": current_user}
    )

def register_device(request: Request, device: EstacioMeteoCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_device = EstacioMeteo(
        nom=device.nom,  # Usamos device.nom porque el esquema mapea "name" a "nom" con alias
        latitude=device.latitude,
        longitude=device.longitude,
        id_empresa=current_user.id_empresa,
        descripcio=device.descripcio,
        ubicacio=device.ubicacio,
        estat=device.estat,
        ip_address=device.ip_address,
        mac_address=device.mac_address,
        versio_firmware=device.versio_firmware
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return templates.TemplateResponse(
        "register_device.html",
        {"request": request, "current_user": current_user, "message": "Dispositivo registrado con éxito"}
    )

def render_device_data_page(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    devices = db.query(EstacioMeteo).filter(EstacioMeteo.id_empresa == current_user.id_empresa).all()
    return templates.TemplateResponse(
        "device_data.html",
        {"request": request, "devices": devices, "current_user": current_user}
    )

def render_device_map_page(request: Request, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    devices = db.query(EstacioMeteo).filter(EstacioMeteo.id_empresa == current_user.id_empresa).all()
    return templates.TemplateResponse(
        "device_map.html",
        {"request": request, "devices": devices, "current_user": current_user}
    )