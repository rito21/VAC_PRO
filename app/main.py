from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers.login import router as login_router
from app.routers.signup import router as sign_router
from app.routers.politica_privacitat import router as politica_privacitat_router
app = FastAPI()

# Montar archivos estáticos (CSS, JS, imágenes, etc.)
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="./templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# @app.get("/login")
# async def login(request: Request):
#     return templates.TemplateResponse("register/login.html", {"request": request})
#


app.include_router(login_router)
app.include_router(sign_router)
app.include_router(politica_privacitat_router)