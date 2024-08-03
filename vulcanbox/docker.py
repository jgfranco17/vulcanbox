import json
import logging
import os
from typing import List

import click
import docker

from .errors import VulcanBoxInputError
from .models import DockerCompose, DockerImage
from .output import print_success, print_warning

logger = logging.getLogger(__name__)


@click.group("new")
def new_group() -> None:
    """Create new images and configurations."""
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


@click.command("image")
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
@click.option(
    "--export-config",
    is_flag=True,
    help="Export the current configurations of the templated Dockerfile",
)
def new_image(name: str, base: str, expose: List[int], build: str, export_config: bool):
    """Initialize a template Dockerfile."""
    # Create project directory if it doesn't exist
    new_file = os.path.join(os.getcwd(), name)
    if os.path.exists(new_file):
        raise VulcanBoxInputError(f"Dockerfile already exists: {new_file}")

    logger.debug(f"Creating new Dockerfile: {name} [base image {base}]")
    if build:
        logger.debug(f"Image will build automatically after {name} is created")
    context = {"base_image": base, "ports": expose}
    image = DockerImage(name, context)
    image.write()
    print_success(f"Created new Dockerfile: {new_file}")

    if build:
        if image.is_built():
            raise VulcanBoxInputError(f"Image already built: {image.image_tag}")
        built_image = image.build(build)
        click.echo(f"Finished building image: {built_image.id}")

    if export_config:
        base_image_used = base.replace(":", "-")
        parsed_name = name.replace(".Dockerfile", "")
        exported_config_file = os.path.join(
            os.getcwd(), f"vulcanbox-{parsed_name}-{base_image_used}.json"
        )
        logger.debug(f"Creating new config file at {exported_config_file}")
        with open(exported_config_file, "w") as json_file:
            json.dump(image.json(), json_file, indent=4)
            click.echo(f"Config JSON exported: {exported_config_file}")


@click.command("compose")
@click.option(
    "--image",
    type=str,
    required=True,
    help="Base Dockerfile to use as image.",
    prompt="Choose a target Dockerfile",
    default="Dockerfile",
)
@click.option(
    "--expose",
    type=int,
    help="Port to expose.",
    prompt="Port to expose (22 for SSH)",
    default=22,
)
@click.option(
    "--count",
    type=int,
    required=True,
    help="Replica count.",
    prompt="Set replica count",
    default=1,
)
@click.option(
    "--with-network",
    is_flag=True,
    help="Link service instances with private network",
)
def new_compose(image: str, expose: int, count: str, with_network: bool) -> None:
    """Initialize a template Docker Compose suite."""
    # Set compose file path to current working dir
    compose_file = os.path.join(os.getcwd(), "docker-compose.yml")

    # Input validation
    if os.path.exists(compose_file):
        if not click.confirm(
            f"Compose file already exists in current directory, overwrite?",
            default=True,
        ):
            print_warning("[USER ABORTED] Compose generation cancelled.")
            return
    image_file = os.path.join(os.getcwd(), image)
    if not os.path.exists(image_file):
        raise VulcanBoxInputError(f"Specified Dockerfile does not exist: {image_file}")
    if count < 1:
        raise VulcanBoxInputError(f"Replica count must at least 1 but got {count}")
    if expose < 1024 and expose != 22:
        raise VulcanBoxInputError(f"Cannot expose port {expose} (privileged)")

    context = {
        "image": image,
        "count": count,
        "port": expose,
        "with_network": with_network,
    }
    logger.debug(f"Creating new Compose file: using '{image}', {count} replicas")
    compose = DockerCompose(context)
    compose.write()
    print_success(f"Created new Docker Compose suite: {compose_file}")


new_group.add_command(new_image)
new_group.add_command(new_compose)
