import logging
from dataclasses import dataclass
from typing import Final

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VulcanBoxFileType:
    """Constants for valid file types."""

    DOCKERFILE: Final[str] = "Dockerfile"
    DOCKER_COMPOSE: Final[str] = "docker-compose.yml"


@dataclass(frozen=True)
class ConsoleIcons:
    """Icons for the shell prints."""

    CHECK: Final[str] = "\u2713"
    CROSS: Final[str] = "\u2715"
