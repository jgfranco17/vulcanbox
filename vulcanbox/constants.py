import logging
from dataclasses import dataclass
from typing import Final

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VulcanBoxFileType:
    """Constants for valid file types."""

    DOCKERFILE: Final[str] = "Dockerfile"
    DOCKER_COMPOSE: Final[str] = "docker-compose.yml"
