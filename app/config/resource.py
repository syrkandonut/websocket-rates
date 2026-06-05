from dataclasses import dataclass

from .utils import load_config


@dataclass(frozen=True, slots=True)
class ResourceConfig:
    api: str


def get_resource_config() -> ResourceConfig:
    api = load_config()['resource']['api']

    return ResourceConfig(
        api=api,
    )
