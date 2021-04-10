# -*- coding: utf8 -*-
import click

from fledgling.cli.config import IniFileConfig


@click.command()
@click.option('--overwrite', default=False, show_default=True, type=click.BOOL)
def create_config(overwrite):
    """
    创建一份空的配置文件。
    """
    config = IniFileConfig()
    config.dump(overwrite)
