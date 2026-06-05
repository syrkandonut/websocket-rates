import tomllib

from pathlib import Path

from . import exceptions as exc

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_PATH = BASE_DIR / 'config.toml'


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise exc.ConfigNotExists()

    with open(CONFIG_PATH, 'rb') as f:
        return tomllib.load(f)
