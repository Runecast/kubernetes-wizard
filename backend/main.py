import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse,JSONResponse
from starlette.exceptions import HTTPException

from routers import router
from config.k8s import cfg


app = FastAPI(
    title='Runecast Kubernetes Wizard',
    openapi_url='/openapi.json',
    docs_url='/docs',
    redoc_url=None
)

if 'BUILD' in os.environ and os.environ['BUILD'] == 'dev':
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

JS_PATH = cfg.path.dist / 'js'
CSS_PATH = cfg.path.dist / 'css'
FAVICON = cfg.path.dist / 'favicon.ico'

if 'BUILD' in os.environ and os.environ['BUILD'] == 'prod':
    app.mount("/js", StaticFiles(directory=JS_PATH), name="js")
    app.mount("/css", StaticFiles(directory=CSS_PATH), name="css")


app.include_router(router)

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    if FAVICON.exists():
        return FileResponse(FAVICON)

@app.get('content')
async def content():
    return JSONResponse({'content': os.walk(top='')})

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):  # noqa
    return RedirectResponse("/")
