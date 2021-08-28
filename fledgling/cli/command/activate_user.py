# -*- coding: utf8 -*-
import click

from fledgling.app.use_case.activate_user import ActivateUserUseCase, IParams
from fledgling.cli.service_factory import ServiceFactory


class Params(IParams):
    def __init__(self, *, activate_code: str, email: str):
        self.activate_code = activate_code
        self.email = email

    def get_activate_code(self) -> str:
        return self.activate_code

    def get_email(self) -> str:
        return self.email


@click.command()
@click.option('--activate-code', help='激活码', required=True, type=click.STRING)
@click.option('--email', help='登录用的邮箱', required=True, type=click.STRING)
@click.pass_context
def activate_user(ctx: click.Context, activate_code: str, email: str):
    """激活用户以便登录。"""
    config = ctx.obj['config']
    service_factory = ServiceFactory(config)
    use_case = ActivateUserUseCase(
        params=Params(
            email=email,
            activate_code=activate_code,
        ),
        user_service=service_factory.user(),
    )
    use_case.run()
