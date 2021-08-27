# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.app.entity.user import IUserRepository
from fledgling.cli.enigma_machine import FernetEnigmaMachine
from fledgling.cli.nest_client import NestClient
from fledgling.repository.location import NestLocationRepository
from fledgling.repository.plan import PlanRepository
from fledgling.repository.task import TaskRepository
from fledgling.repository.user import NestUserRepository


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


class RepositoryFactory:
    def __init__(self, config):
        assert isinstance(config, IConfig)
        enigma_machine_section = config['enigma_machine']
        enigma_machine = FernetEnigmaMachine(enigma_machine_section['password'])
        self.enigma_machine = enigma_machine
        nest_section = config['nest']
        hostname = nest_section['hostname']
        port = nest_section['port']
        protocol = nest_section['protocol']
        cookies_path = nest_section['cookies_path']
        account_section = config['account']
        email = account_section['email']
        password = account_section['password']
        nest_client = NestClient(
            cookies_path=cookies_path,
            email=email,
            hostname=hostname,
            password=password,
            port=port,
            protocol=protocol,
        )
        self.nest_client = nest_client

    def for_location(self):
        return NestLocationRepository(
            nest_client=self.nest_client,
        )

    def for_plan(self):
        return PlanRepository(
            nest_client=self.nest_client,
        )

    def for_task(self):
        return TaskRepository(
            enigma_machine=self.enigma_machine,
            nest_client=self.nest_client,
        )

    def for_user(self) -> IUserRepository:
        return NestUserRepository(
            nest_client=self.nest_client,
        )
