# -*- coding: utf8 -*-
from fledgling.app.use_case.create_task import CreateTaskUseCase, IParams
from fledgling.cli.config import config
from fledgling.cli.enigma_machine import FernetEnigmaMachine
from fledgling.cli.nest_client import NestClient
from fledgling.repository.task import TaskRepository


class Params(IParams):
    def __init__(self, *, brief):
        self.brief = brief

    def get_brief(self) -> str:
        return self.brief


def create_task(*, brief):
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
    params = Params(
        brief=brief,
    )
    task_repository = TaskRepository(
        nest_client=nest_client,
    )
    use_case = CreateTaskUseCase(
        params=params,
        task_repository=task_repository,
    )
    use_case.run()
