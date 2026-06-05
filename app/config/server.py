from dataclasses import dataclass

from .utils import load_config


@dataclass(frozen=True, slots=True)
class ServerConfig:
    host: str
    port: int


def get_server_config() -> ServerConfig:
    host = load_config()['server']['host']
    port = load_config()['server']['port']

    return ServerConfig(
        host=host,
        port=port,
    )
