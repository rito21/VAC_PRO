from typing import Annotated

from fastapi import FastAPI, Request, Cookie, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.settings import COOKIE_NAME, settings
from app.dependencies import get_db
from app.routers.login import router as login_router
from app.routers.signup import router as signup_router
from app.routers.usuari import router as usuaris_router
from app.auth.login import verify_token, get_current_user
from app.version import __version__

mode = 'test'

app = FastAPI(
    title="Simple login example",
    description="A simple login example with a private section",
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url='/docs' if not settings.TESTING else None,
    redoc_url='/redoc' if not settings.TESTING else None,
)

if not settings.TESTING:
    app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")

    # Gestió de l'error 404
    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, exc):
        """
        Gestor d'exceptions asíncron per a StarletteHTTPException que retorna una resposta HTTP personalitzada.
        Gestiona l'error 404 i mostra una pàgina d'error personalitzada.

        Paràmetres:
            - request: L'objecte de petició entrant.
            - exc: La instància de StarletteHTTPException.

        Retorn:
            - Si el codi d'estat de l'excepció és HTTP 404 Not Found, retorna una TemplateResponse amb la plantilla "404.html" i l'objecte de petició, amb un codi d'estat de HTTP 404 Not Found.
        """
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            return templates.TemplateResponse("404.html", {"request": request}, status_code=status.HTTP_404_NOT_FOUND)

# Routers
app.include_router(login_router)
app.include_router(signup_router)
app.include_router(usuaris_router)


@app.get("/", response_class=HTMLResponse)
# async def read_home(request: Request, token: str = Depends(oauth2_scheme)):
async def read_home(request: Request,
                    access_token: Annotated[str | None, Cookie()] = None,
                    db: Session = Depends(get_db)):
    is_authenticated = False
    if access_token is not None:
        valid_token = verify_token(access_token)
        if valid_token:
            if get_current_user(db=db, token=access_token) is not None:
                is_authenticated = True
    return templates.TemplateResponse("index.html", {"request": request, "is_authenticated": is_authenticated})


@app.post("/logout", response_class=HTMLResponse)
def logout():
    return RedirectResponse("/",
                            status_code=status.HTTP_302_FOUND,
                            headers={"set-cookie": f"{COOKIE_NAME}=; Max-Age=-1"}  # Invalidem el token
                            )
