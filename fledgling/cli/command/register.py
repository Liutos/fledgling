# -*- coding: utf8 -*-
import click

from fledgling.app.use_case.create_user import CreateUserUseCase, IParams
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, email: str, nickname: str, password: str):
        self.email = email
        self.nickname = nickname
        self.password = password

    def get_email(self) -> str:
        return self.email

    def get_nickname(self) -> str:
        return self.nickname

    def get_password(self) -> str:
        return self.password


@click.command()
@click.option('--email', help='登录用的邮箱', required=True, type=click.STRING)
@click.option('--nickname', help='昵称', required=True, type=click.STRING)
@click.option('--password', help='登录所需的密码', required=True, type=click.STRING)
def register(email: str, nickname: str, password: str):
    """注册一个新用户。"""
    config = IniFileConfig()
    config.load()
    repository_factory = RepositoryFactory(
        config=config,
    )
    use_case = CreateUserUseCase(
        params=Params(
            email=email,
            nickname=nickname,
            password=password,
        ),
        user_repository=repository_factory.for_plan(),
    )
    use_case.run()
