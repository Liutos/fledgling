# -*- coding: utf8 -*-
import click
import daemon
import datetime
from typing import Optional

from fledgling.app.entity.location import InvalidLocationError
from fledgling.app.use_case.event_loop import (
    EventLoopUseCase,
    IParams,
)
from fledgling.cli.alerter import Alerter, FacadeAlerter, ServerChanAlerter
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory
from fledgling.cli.service_factory import ServiceFactory


class Params(IParams):
    def __init__(self, *, config: IniFileConfig):
        self.config = config

    def get_do_not_disturb_begin_time(self) -> Optional[datetime.time]:
        textual_begin_time: Optional[str] = self.config.get('do_not_disturb', 'begin_time')
        if textual_begin_time is None:
            return None

        return datetime.datetime.strptime(textual_begin_time, '%H:%M').time()

    def get_do_not_disturb_end_time(self) -> Optional[datetime.time]:
        textual_end_time: Optional[str] = self.config.get('do_not_disturb', 'end_time')
        if textual_end_time is None:
            return None

        return datetime.datetime.strptime(textual_end_time, '%H:%M').time()

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
    service_factory = ServiceFactory(config)
    do_not_disturb_service = service_factory.get_do_not_disturb_service()
    # 实例化一个发通知的对象。
    wechat_alerter = ServerChanAlerter(
        channels=config.get('sc').get('channels').split(','),
        send_key=config.get('sc').get('send_key'),
    )
    alerter = FacadeAlerter(Alerter(), wechat_alerter)

    use_case = EventLoopUseCase(
        alerter=alerter,
        do_not_disturb_service=do_not_disturb_service,
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
