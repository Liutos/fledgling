# -*- coding: utf8 -*-
import click
import logging

from xdg import xdg_data_home

from fledgling.cli.command.create_config import create_config
from fledgling.cli.command.create_plan import create_plan
from fledgling.cli.command.create_task import create_task
from fledgling.cli.command.delete_plan import delete_plan
from fledgling.cli.command.event_loop import event_loop
from fledgling.cli.command.list_plan import list_plan
from fledgling.cli.command.list_task import list_task

cli = click.Group()

cli.add_command(create_config)

cli.add_command(create_plan)

cli.add_command(create_task)

cli.add_command(delete_plan)

cli.add_command(event_loop)

cli.add_command(list_plan)

cli.add_command(list_task)

log_dir = xdg_data_home().joinpath('fledgling')
if not log_dir.is_dir():
    log_dir.mkdir()
log_file = log_dir.joinpath('fledgling.log')
logging.basicConfig(
    filename=str(log_file),
    format='%(levelname)s:%(asctime)s:%(message)s',
)


if __name__ == '__main__':
    cli()
