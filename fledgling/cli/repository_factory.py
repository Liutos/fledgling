# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.cli.enigma_machine import FernetEnigmaMachine
from fledgling.cli.nest_client import NestClient
from fledgling.repository.plan import PlanRepository
from fledgling.repository.task import TaskRepository


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
        nest_section = config['nest']
        hostname = nest_section['hostname']
        port = nest_section['port']
        protocol = nest_section['protocol']
        nest_client = NestClient(
            enigma_machine=enigma_machine,
            hostname=hostname,
            port=port,
            protocol=protocol,
        )
        account_section = config['account']
        email = account_section['email']
        password = account_section['password']
        nest_client.login(
            email=email,
            password=password,
        )
        self.nest_client = nest_client

    def for_plan(self):
        return PlanRepository(
            nest_client=self.nest_client,
        )

    def for_task(self):
        return TaskRepository(
            nest_client=self.nest_client,
        )
