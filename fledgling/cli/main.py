# -*- coding: utf8 -*-
from typing import Optional

import click
import logging.handlers

from xdg import xdg_data_home

from fledgling.cli.command.activate_user import activate_user
from fledgling.cli.command.change_location import change_location
from fledgling.cli.command.change_plan import change_plan
from fledgling.cli.command.change_task import change_task
from fledgling.cli.command.create_config import create_config
from fledgling.cli.command.create_location import create_location
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
from fledgling.cli.command.send_message import send_message
from fledgling.cli.config import IniFileConfig


@click.group()
@click.option('--config-file', default=IniFileConfig.get_default_config_file(), help='配置文件路径', show_default=True)
@click.option('--json', 'is_json', default=False, help='是否以 JSON 格式输出结果', is_flag=True, type=click.BOOL)
@click.pass_context
def cli(ctx: click.Context, *, config_file: Optional[str],
        is_json: bool):
    config = IniFileConfig(config_file=config_file)
    config.load()
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['is_json'] = is_json


cli.add_command(activate_user)
cli.add_command(change_location)
cli.add_command(change_plan)
cli.add_command(change_task)
cli.add_command(create_config)

cli.add_command(create_location)
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
cli.add_command(send_message)

log_dir = xdg_data_home().joinpath('fledgling')
if not log_dir.is_dir():
    log_dir.mkdir(parents=True)
log_file = log_dir.joinpath('fledgling.log')
handler = logging.handlers.TimedRotatingFileHandler(
    filename=str(log_file),
    when='D',
)
kwargs = dict(
    format='%(levelname)s:%(asctime)s:%(message)s',
    handlers=[handler],
    # TODO: 应当支持通过配置文件修改level。
    level=logging.DEBUG,
)
logging.basicConfig(**kwargs)


if __name__ == '__main__':
    cli()
