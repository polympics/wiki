"""Settings for the compiler."""
import json
import pathlib


BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()

try:
    with open(BASE_DIR / 'config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}


def get_path(name: str, default: pathlib.Path) -> pathlib.Path:
    """Get a path from the config, or use a default."""
    if name in config:
        return pathlib.Path(config[name])
    return default


IN_DIR = get_path('in', BASE_DIR / 'content').absolute()
OUT_DIR = get_path('out', BASE_DIR / 'out').absolute()
INDEX_FILE = config.get('index_file', 'index.json')
