# -*- coding: utf8 -*-
import click
import daemon
from typing import Optional

from fledgling.app.entity.location import InvalidLocationError
from fledgling.app.use_case.event_loop import (
    EventLoopUseCase,
    IParams,
)
from fledgling.cli.alerter import Alerter, FacadeAlerter, ServerChanAlerter
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, config: IniFileConfig):
        self.config = config

    def get_location_name(self) -> Optional[str]:
        return self.config['location']['name']


@click.command()
@click.option('--is-daemon', default=False, help='以守护进程运行', is_flag=True, type=click.BOOL)
@click.pass_context
def event_loop(ctx: click.Context, is_daemon: bool):
    """
    启动事件循环拉取计划并弹出提醒。
    """
    config: IniFileConfig = ctx.obj['config']
    repository_factory = RepositoryFactory(
        config=config,
    )
    location_repository = repository_factory.for_location()
    params = Params(config=config)
    plan_repository = repository_factory.for_plan()
    task_repository = repository_factory.for_task()
    # 实例化一个发通知的对象。
    wechat_alerter = ServerChanAlerter(
        channels=config.get('sc').get('channels').split(','),
        send_key=config.get('sc').get('send_key'),
    )
    alerter = FacadeAlerter(Alerter(), wechat_alerter)

    use_case = EventLoopUseCase(
        alerter=alerter,
        location_repository=location_repository,
        params=params,
        plan_repository=plan_repository,
        task_repository=task_repository,
    )
    try:
        if is_daemon:
            with daemon.DaemonContext():
                use_case.run()
        else:
            use_case.run()
    except InvalidLocationError as e:
        print('没有名为{}的地点'.format(e.name))
