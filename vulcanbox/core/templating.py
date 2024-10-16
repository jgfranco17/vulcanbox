import logging
import os
from typing import Dict, Optional

from jinja2 import Environment, FileSystemLoader

from vulcanbox.core.errors import VulcanBoxInputError

logger = logging.getLogger(__name__)


class BaseTemplatedFile:
    """Base class for templated files."""

    def __init__(
        self,
        name: str,
        src: str,
        file_type: str,
        context: Dict[str, str],
        whitespace: Optional[bool] = True,
    ) -> None:
        if file_type not in name:
            raise VulcanBoxInputError(f"Name is invalid, must end with 'Dockerfile'")
        self.__name = name
        self.__file_type = file_type
        self.template_src = src
        self.template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.source = os.path.join(self.template_dir, src)
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=False,
            lstrip_blocks=False,
        )
        self.context = context
        self.whitespace = whitespace
        self.__destination = os.path.join(os.getcwd(), self.__name)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def destination(self) -> str:
        return self.__destination

    def __render_template(self, file: str) -> str:
        """Render a template file with the given context."""
        template = self.env.get_template(file)
        rendered_content = template.render(self.context)
        if not self.whitespace:
            rendered_content.replace("\n", "")
        if not rendered_content.endswith("\n"):
            rendered_content += "\n"
        return rendered_content

    def write(self) -> None:
        """Write the contents to file."""
        with open(self.__destination, "w") as f:
            file_content = self.__render_template(
                f"{self.template_src}/{self.__file_type}.j2"
            )
            f.write(file_content)
            logger.info(f"Wrote to file: {self.__destination}")
