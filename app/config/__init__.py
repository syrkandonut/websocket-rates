from dataclasses import dataclass

from .server import get_server_config, ServerConfig
from .resource import get_resource_config, ResourceConfig
from .rate import get_rate_config, RateConfig


@dataclass(frozen=True, slots=True)
class Settings:
    server: ServerConfig
    resource: ResourceConfig
    rate: RateConfig


def get_settings() -> Settings:
    return Settings(
        server=get_server_config(),
        resource=get_resource_config(),
        rate=get_rate_config(),
    )
