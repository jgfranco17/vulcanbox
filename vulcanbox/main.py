import logging

import click
import colorama

from vulcanbox import __version__
from vulcanbox.core.handler import VulcanBoxCliHandler
from vulcanbox.core.output import ColorHandler
from vulcanbox.doctor import doctor
from vulcanbox.new import new_group

colorama.init(autoreset=True)


def __get_log_level(verbosity: int) -> int:
    levels = {0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}
    return levels.get(verbosity, logging.DEBUG)


def __set_logger(level: int):
    logger = logging.getLogger(__package__)
    log_level = __get_log_level(level)
    logger.setLevel(log_level)
    handler = ColorHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter(
        fmt="[%(asctime)s][%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(handler)


@click.group(cls=VulcanBoxCliHandler)
@click.pass_context
@click.version_option(version=__version__)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity. Use multiple times for more detail (e.g., -vv for debug).",
)
def cli(context: click.Context, verbose: int):
    """VulcanBox: CLI tool for managing containers and virtual machines."""
    __set_logger(verbose)
    context.ensure_object(dict)


cli.add_command(new_group)
cli.add_command(doctor)
