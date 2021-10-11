# -*- coding: utf8 -*-
from typing import Optional

import click
import logging

from xdg import xdg_data_home

from fledgling.cli.command.activate_user import activate_user
from fledgling.cli.command.change_plan import change_plan
from fledgling.cli.command.change_task import change_task
from fledgling.cli.command.create_config import create_config
from fledgling.cli.command.create_plan import create_plan
from fledgling.cli.command.create_task import create_task
from fledgling.cli.command.register import register
from fledgling.cli.command.delete_location import delete_location
from fledgling.cli.command.delete_plan import delete_plan
from fledgling.cli.command.delete_task import delete_task
from fledgling.cli.command.event_loop import event_loop
from fledgling.cli.command.list_location import list_location
from fledgling.cli.command.list_plan import list_plan
from fledgling.cli.command.list_task import list_task
from fledgling.cli.config import IniFileConfig


@click.group()
@click.option('--config-file', help='配置文件路径')
@click.pass_context
def cli(ctx: click.Context, *, config_file: Optional[str]):
    config = IniFileConfig(config_file=config_file)
    config.load()
    ctx.ensure_object(dict)
    ctx.obj['config'] = config


cli.add_command(activate_user)
cli.add_command(change_plan)
cli.add_command(change_task)
cli.add_command(create_config)

cli.add_command(create_plan)

cli.add_command(create_task)
cli.add_command(delete_location)
cli.add_command(delete_plan)
cli.add_command(delete_task)
cli.add_command(event_loop)
cli.add_command(list_location)
cli.add_command(list_plan)

cli.add_command(list_task)
cli.add_command(register)

log_dir = xdg_data_home().joinpath('fledgling')
if not log_dir.is_dir():
    log_dir.mkdir(parents=True)
log_file = log_dir.joinpath('fledgling.log')
logging.basicConfig(
    filename=str(log_file),
    format='%(levelname)s:%(asctime)s:%(message)s',
    # TODO: 应当支持通过配置文件修改level。
    level=logging.DEBUG,
)


if __name__ == '__main__':
    cli()
