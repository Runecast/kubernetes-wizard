from pathlib import Path
from pydantic import BaseModel


LEVELS_FROM_ROOT = 2  # Depth of the current file relative to the root of the project
DATA = 'data'
APP_BACKEND = 'backend'
APP_FRONTEND = 'frontend'

CURRENT_FILE = Path(__file__).resolve()  # Absolute path of the current file
ROOT_DIR = CURRENT_FILE.parents[LEVELS_FROM_ROOT]  # Root of the project

DATA_DIR = ROOT_DIR / DATA
APP_BACKEND_DIR = ROOT_DIR / APP_BACKEND
APP_FRONTEND_DIR = ROOT_DIR / APP_FRONTEND


class PathConfig(BaseModel):
    root: Path = ROOT_DIR
    data: Path = DATA_DIR
    backend: Path = APP_BACKEND_DIR
    frontend: Path = APP_FRONTEND_DIR
    dist: Path = APP_FRONTEND_DIR / 'dist'
    k8s_api_data_prefix: str = 'k8s_api'


class ModificationsConfig(BaseModel):
    cache_ttl: int = 600  # Time To Live in seconds (for timed_lru_cache decorator)


class ActionConfig(BaseModel):
    set_scalar: str = 'set scalar'
    set_list: str = 'set list'
    append: str = 'append scalar'
    concatenate: str = 'concatenate list'
    drop: str = 'drop attribute'
    remove: str = 'remove items'


class VersionsConfig(BaseModel):
    latest: str = 'v1-25'
    old: list[str] = [
        'v1-24',
        'v1-23',
        'v1-22',
        'v1-21',
        'v1-20',
    ]


class Config(BaseModel):
    path = PathConfig()
    api_modifications = ModificationsConfig()
    action = ActionConfig()
    versions = VersionsConfig()


cfg = Config()
