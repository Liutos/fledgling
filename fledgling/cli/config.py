# -*- coding: utf8 -*-
import configparser
import os

from xdg import xdg_config_home

from fledgling.cli.repository_factory import IConfig


class IniFileConfig(IConfig):
    """
    基于.ini文件的配置。
    """
    def __init__(self):
        config_dir = xdg_config_home().joinpath('fledgling')
        config_file = config_dir.joinpath('config.ini')
        print('config_file', config_file)
        self.config = configparser.ConfigParser()
        self.config_dir = config_dir
        self.config_file = config_file

    def dump(self, is_overwrite):
        if not self.config_dir.is_dir():
            self.config_dir.mkdir()
        if not is_overwrite and self.config_file.is_file():
            print('文件{}已存在。'.format(str(self.config_file)))
            exit(1)

        current_dir = os.path.dirname(__file__)
        sample_file_path = os.path.join(current_dir, 'config/sample.ini')
        with open(sample_file_path) as f:
            self.config_file.write_text(f.read())

    def get(self, *keys):
        result = self.config
        for key in keys:
            result = result[key]
        return result

    def load(self):
        if not self.config_dir.is_dir():
            print('找不到目录{}'.format(self.config_dir))
            exit(1)

        if not self.config_file.is_file():
            print('找不到文件{}'.format(self.config_file))
            exit(1)

        self.config.read(self.config_file)
        print('config.sections()', self.config.sections())
