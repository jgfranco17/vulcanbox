import logging
import subprocess
from dataclasses import dataclass
from typing import List, Tuple

import click

from vulcanbox.core.constants import ConsoleIcons
from vulcanbox.core.errors import VulcanBoxRuntimeError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CliDependency:
    name: str
    command: str
    version_flag: str
    install_guide: str


@click.command("doctor")
def doctor():
    tools = [
        CliDependency(
            name="Docker",
            command="docker",
            version_flag="--version",
            install_guide="https://docs.docker.com/get-started/get-docker/",
        ),
        CliDependency(
            name="Docker Compose",
            command="docker compose",
            version_flag="version",
            install_guide="https://docs.docker.com/compose/install/",
        ),
        CliDependency(
            name="Git",
            command="git",
            version_flag="--version",
            install_guide="https://git-scm.com/book/en/v2/Getting-Started-Installing-Git",
        ),
    ]

    missing_dependencies: List[CliDependency] = []
    click.echo("Vulcanbox Doctor:")
    for tool in tools:
        installed, version = __get_bin_version(f"{tool.command} {tool.version_flag}")
        if installed:
            click.secho(f"[{ConsoleIcons.CHECK}] {version}", fg="green")
        else:
            click.secho(f"[{ConsoleIcons.CROSS}] {tool.name} not installed", fg="red")
            missing_dependencies.append(tool)

    print("-" * 20)
    if missing_dependencies:
        click.secho(
            f"Vulcanbox Doctor found {len(missing_dependencies)} missing dependencies!",
            fg="yellow",
        )
        for dep in missing_dependencies:
            click.echo(f"- Install {dep.name} from {dep.install_guide}")
    else:
        click.echo(f"All {len(tools)} dependencies ready!")


def __get_bin_version(command: str) -> Tuple[bool, str]:
    """Split the input string by spaces and return the rightmost substring."""
    try:
        result = subprocess.run(
            command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            raise VulcanBoxRuntimeError(
                f"Running '{command}' returned exit code: {result.exit_code}"
            )
        return True, result.stdout.decode("utf-8").strip()
    except (subprocess.CalledProcessError, VulcanBoxRuntimeError):
        return False, ""
