# -*- coding: utf8 -*-
import click

from fledgling.app.use_case.send_message import IParams, SendMessageUseCase
from fledgling.cli.config import IniFileConfig
from fledgling.service.server_chan_service import ServerChanService, ServerChanServiceConfig


class CLIParams(IParams):
    def __init__(self, *, desp: str, title: str):
        self._desp = desp
        self._title = title

    def get_desp(self) -> str:
        return self._desp

    def get_title(self) -> str:
        return self._title


@click.command()
@click.option('-d', '--desp', default='', help='消息内容')
@click.option('-t', '--title', help='消息标题', required=True)
@click.pass_context
def send_message(ctx: click.Context, desp, title):
    """通过 Server 酱 Turbo 版发送消息。"""
    config: IniFileConfig = ctx.obj['config']
    SendMessageUseCase(
        params=CLIParams(
            desp=desp,
            title=title,
        ),
        server_chan_service=ServerChanService(
            config=ServerChanServiceConfig(
                config.get('sc', 'send_key'),
            )
        )
    ).run()
