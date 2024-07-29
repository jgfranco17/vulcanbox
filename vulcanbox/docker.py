import logging
import os
from typing import List

import click
import docker

from .constants import Environment
from .errors import VulcanBoxInputError, VulcanBoxRuntimeError
from .models import DockerImage
from .output import print_error, print_success

logger = logging.getLogger(__name__)


@click.group("docker")
def docker_group() -> None:
    """Interact with Docker images and containers."""
    pass


def __validate_directory(ctx: click.Context, param: click.Parameter, value: str) -> str:
    if value and not os.path.isdir(value):
        raise VulcanBoxInputError(
            f"The directory '{value}' does not exist or is not a directory."
        )
    return value


def __build_docker_image(dockerfile_path: str, image_name: str) -> None:
    """Build the Docker image from the Dockerfile."""
    client = docker.from_env()
    try:
        image, logs = client.images.build(
            path=os.path.dirname(dockerfile_path),
            dockerfile=os.path.basename(dockerfile_path),
            tag=image_name,
        )
        for log in logs:
            logger.info(log.get("stream", "").strip())
        logger.info(f"Docker image {image_name} built successfully.")
    except docker.errors.BuildError as e:
        logger.error(f"Error building Docker image: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


@click.command("new")
@click.option(
    "--name",
    type=str,
    required=True,
    help="Name of Dockerfile",
    prompt="Set a name for the Dockerfile",
    default="new.Dockerfile",
)
@click.option(
    "--base",
    type=str,
    required=True,
    help="Base image to use.",
    prompt="Choose a base image",
    default="ubuntu:20.04",
)
@click.option(
    "--build",
    type=str,
    required=True,
    help="Build the image after templating",
    default="",
)
@click.option(
    "--expose", multiple=True, type=int, help="Ports to expose in the Dockerfile"
)
def new(name: str, base: str, expose: List[int], build: str):
    """Initialize a template Dockerfile."""
    # Create project directory if it doesn't exist
    new_file = os.path.join(os.getcwd(), name)
    if os.path.exists(new_file):
        raise VulcanBoxInputError(f"Dockerfile already exists: {new_file}")
    context = {"base_image": base, "ports": expose}
    image = DockerImage(name, expose, context)
    image.write()
    print_success(f"Created new Dockerfile: {new_file}")

    if build:
        built_image = image.build(build)
        click.echo(f"Finished building image: {built_image.id}")


docker_group.add_command(new)
