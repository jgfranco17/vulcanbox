import datetime as dt
import logging
from typing import Any, Dict, List, Optional

import click
import docker
from tqdm import tqdm

from .templating import BaseTemplatedFile

logger = logging.getLogger(__name__)


class DockerImage(BaseTemplatedFile):
    """Template engine for repositories."""

    def __init__(self, name: str, ports: List[int], context: Dict[str, str]) -> None:
        self.client = docker.from_env()
        self.ports = ports or []
        super().__init__(name=name, src="docker", context=context)
        self.image_tag = None

    def is_built(self) -> bool:
        return self.image_tag is not None

    def json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "tag": self.image_tag,
            "ports": self.ports,
            "context": self.context,
        }

    @staticmethod
    def __get_image_name(base_name: str) -> str:
        now = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        sanitized_name = base_name.replace(" ", "-").replace("/", "-")
        return f"vulcanbox-{sanitized_name}-{now}"

    def build(self, name: Optional[str] = ""):
        """Build the Docker image."""
        self.image_tag = self.__get_image_name(name)
        image, logs = self.client.images.build(
            path=".",
            dockerfile=self.destination,
            tag=self.image_tag,
            nocache=True,
            rm=True,
            forcerm=True,
        )
        for log in tqdm(logs, desc=f"Building [{self.image_tag}]"):
            if "stream" in log:
                click.echo(log["stream"].strip())
        return image

    def start(self) -> None:
        """Run the Docker container."""
        container = self.client.containers.run(
            self.name, name=self.container_name, remove=True, detach=True
        )
        print(container.logs().decode("utf-8"))
        return container
