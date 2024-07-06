# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Optional
import configparser
import os
import pathlib

from xdg import xdg_config_home


class IConfig(ABC):
    def __getitem__(self, item):
        return self.get(item)

    @abstractmethod
    def dump(self, is_overwrite):
        """
        将配置持久化存储。
        """
        pass

    @abstractmethod
    def get(self, *keys):
        pass

    @abstractmethod
    def load(self):
        """
        加载配置。
        """
        pass


# FIXME: 具体实现不应当和抽象接口放在一起。
class IniFileConfig(IConfig):
    """
    基于.ini文件的配置。
    """
    def __init__(self, *, config_file: Optional[str] = None):
        if config_file:
            self.config_file = pathlib.Path(config_file)
        else:
            self.config_file = self.get_default_config_file()

        self.config = configparser.ConfigParser()
        self.config_dir = self.get_default_config_dir()

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
            if key not in result:
                return None

            result = result[key]
        return result

    @classmethod
    def get_default_config_dir(cls):
        """配置文件所在的默认目录。"""
        return xdg_config_home().joinpath('fledgling')

    @classmethod
    def get_default_config_file(cls):
        """默认配置文件。"""
        default_config_dir = cls.get_default_config_dir()
        return default_config_dir.joinpath('config.ini')

    def load(self):
        if not self.config_dir.is_dir():
            print('找不到目录{}'.format(self.config_dir))
            exit(1)

        if not self.config_file.is_file():
            print('找不到文件{}'.format(self.config_file))
            exit(1)

        self.config.read(self.config_file)
