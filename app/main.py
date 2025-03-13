from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db, init_db
from app.auth.login import get_current_user, get_current_user_no_db
from app.models.usuari import Usuari
from app.routers.login import router as login_router
from app.routers.signup import router as sign_router

from app.routers.contacte import router as contacte_router
from app.routers.public import router as public_router
from app.routers.politica_cookies import router as politica_cookies_router
from app.utils.dashboard import render_dashboard, render_register_device_page, register_device, render_device_data_page, render_device_map_page
from sqlalchemy.orm import configure_mappers

# Importamos los modelos para asegurarnos de que estén registrados
from app.models.empresa import DbEmpresa
from app.models.usuari import Usuari
from app.models.config import TblConfig
from app.models.device import Device
from app.models.measurement import Measurement
from app.models.empresa import DbEmpresa
from app.models.usuari import Usuari
from app.models.estacio_meteo import EstacioMeteo
from app.models.lectura import Lectura
from app.models.tipus_sensor import TipusSensor
from app.models.sensor import Sensor
from app.models.config import TblConfig
from app.models.app_config import AppConfig
from app.models.device import Device
from app.models.measurement import Measurement
# Forzamos la configuración de los mapeadores después de importar todos los modelos
configure_mappers()

# Inicializamos la base de datos
init_db()

app = FastAPI(debug=True)

app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")

@app.middleware("http")
async def add_user_to_templates(request: Request, call_next):
    """Middleware para incluir `user` en cada template"""
    user = None
    try:
        user = await get_current_user(request.cookies.get("access_token"), db=next(get_db()))
    except:
        pass  # Usuario no autenticado

    request.state.user = user
    response = await call_next(request)
    return response

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": request.state.user})


# Importamos los routers después de inicializar los modelos y la base de datos
app.include_router(login_router)
app.include_router(sign_router)

app.include_router(contacte_router)
app.include_router(public_router)
app.include_router(politica_cookies_router)

# Rutas del dashboard y dispositivos
@app.get("/dashboard/", response_model=None)
async def dashboard(request: Request, current_user: Usuari = Depends(get_current_user_no_db)):
    return render_dashboard(request, current_user)

@app.get("/dashboard/devices/register", response_model=None)
async def register_device_page(request: Request, current_user: Usuari = Depends(get_current_user_no_db)):
    return render_register_device_page(request, current_user)

@app.post("/dashboard/devices/register", response_model=None)
async def register_device_endpoint(
    request: Request,
    name: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    current_user: Usuari = Depends(get_current_user),  # Este endpoint necesita db para registrar el dispositivo
    db: Session = Depends(get_db)
):
    return register_device(request, current_user, name, latitude, longitude, db)

@app.get("/dashboard/devices/data", response_model=None)
async def device_data_page(request: Request, current_user: Usuari = Depends(get_current_user_no_db)):
    return render_device_data_page(request, current_user)

@app.get("/dashboard/devices/map", response_model=None)
async def device_map_page(request: Request, current_user: Usuari = Depends(get_current_user_no_db)):
    return render_device_map_page(request, current_user)

