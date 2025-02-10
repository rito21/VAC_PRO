from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Montar archivos estáticos (CSS, JS, imágenes, etc.)
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Configurar la carpeta de plantillas
templates = Jinja2Templates(directory="./templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

