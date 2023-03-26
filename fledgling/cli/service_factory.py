# -*- coding: utf8 -*-
from fledgling.app.use_case.activate_user import IUserService
from fledgling.app.use_case.event_loop import IDoNotDisturbService
from fledgling.cli.config import IConfig
from fledgling.cli.enigma_machine import FernetEnigmaMachine
from fledgling.cli.nest_client import NestClient
from fledgling.service.do_not_disturb import DoNotDisturbService
from fledgling.service.user import NestUserService


class ServiceFactory:
    def __init__(self, config):
        # TODO: 这里和 repository_service 中的代码重复了，说明 nest_client 也应当由外部传入。
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

    def get_do_not_disturb_service(self) -> IDoNotDisturbService:
        return DoNotDisturbService()

    def user(self) -> IUserService:
        return NestUserService(
            nest_client=self.nest_client,
        )
