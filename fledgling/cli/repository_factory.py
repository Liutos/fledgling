# -*- coding: utf8 -*-
from fledgling.cli.config import config
from fledgling.cli.enigma_machine import FernetEnigmaMachine
from fledgling.cli.nest_client import NestClient
from fledgling.repository.plan import PlanRepository
from fledgling.repository.task import TaskRepository

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


class RepositoryFactory:
    @classmethod
    def for_plan(cls):
        return PlanRepository(
            nest_client=nest_client,
        )

    @classmethod
    def for_task(cls):
        return TaskRepository(
            nest_client=nest_client,
        )
