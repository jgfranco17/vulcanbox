"""Init docker command group."""
import click

from vulcanbox.new.docker import new_compose, new_image


@click.group("new")
def new_group() -> None:
    """Create new images and configurations."""
    pass


new_group.add_command(new_image)
new_group.add_command(new_compose)
