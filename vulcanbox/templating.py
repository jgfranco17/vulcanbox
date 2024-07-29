import logging
from typing import Dict, List

import click
import docker

from .models import BaseTemplatedFile

logger = logging.getLogger(__name__)


class DockerImage(BaseTemplatedFile):
    """Template engine for repositories."""

    def __init__(self, name: str, ports: List[int], context: Dict[str, str]) -> None:
        self.client = docker.from_env()
        self.ports = ports or []
        super().__init__(name=name, src="docker", context=context)

    def build(self):
        """Build the Docker image."""
        image, logs = self.client.images.build(path=".", tag=self.image_name)
        for log in logs:
            if "stream" in log:
                click.echo(log["stream"].strip())
        return image

    def start(self) -> None:
        """Run the Docker container."""
        container = self.client.containers.run(
            self.image_name, name=self.container_name, remove=True, detach=True
        )
        print(container.logs().decode("utf-8"))
        return container
