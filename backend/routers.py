from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse


from src.fetch_data import fetch_data
from config.k8s import cfg
from src.modifications.validation import modifications_data


router = APIRouter()


@router.get('/api_reference/{version}', response_class=JSONResponse)
async def get_data(version: str):
    if version == 'latest':
        version = cfg.versions.latest
    file_name = f'{cfg.path.k8s_api_data_prefix}_{version}.json'
    file_path = cfg.path.data / file_name
    data = fetch_data(file_path)
    return JSONResponse(content=data)


@router.get('/modifications', response_class=JSONResponse)
async def get_modifications():
    return JSONResponse(content=modifications_data)


@router.get('/', response_class=HTMLResponse)
async def serve_front_end():
    index = cfg.path.dist / 'index.html'
    if index.exists():
        return index.read_text()
    else:
        print('Page not found')
