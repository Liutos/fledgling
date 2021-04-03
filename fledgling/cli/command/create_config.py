# -*- coding: utf8 -*-
from fledgling.cli.config import IniFileConfig


def create_config(overwrite):
    """
    创建一份空的配置文件。
    """
    config = IniFileConfig()
    config.dump(overwrite)
