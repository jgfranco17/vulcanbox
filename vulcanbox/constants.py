import logging
import os
from typing import Any, Final

from .errors import VulcanBoxInputError

logger = logging.getLogger(__name__)


class Variable:
    """Store environment variables."""

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__value = os.getenv(name)
        logger.debug(f"Loaded environment variable {name}")

    def __repr__(self) -> str:
        displayed_value = "'NOT SET'" if self.__value is None else "*****"
        return f"<Variable name={self.__name} value={displayed_value}>"

    def __bool__(self) -> bool:
        return self.__value is not None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> Any:
        return self.__value

    def validate(self) -> None:
        if self.__value is None:
            raise VulcanBoxInputError(
                f"Environment variable '{self.__name}' is not set"
            )
        logger.info(f"Validated environment variable '{self.__name}'")


class Environment:
    """Constants for environment variables."""

    GITHUB_USERNAME = Variable("GITHUB_USERNAME")
    GITHUB_API_TOKEN = Variable("GITHUB_API_TOKEN")


class LoggerFormats:
    """Fromatting strings for datetime formats."""

    MESSAGE_FORMAT: Final[str] = "[%(asctime)s][%(levelname)s] %(name)s: %(message)s"
    DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
