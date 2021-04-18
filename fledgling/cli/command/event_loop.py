# -*- coding: utf8 -*-
import click
import daemon

from fledgling.app.use_case.event_loop import EventLoopUseCase
from fledgling.cli.alerter import Alerter
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


@click.command()
@click.option('--is-daemon', default=False, help='以守护进程运行', is_flag=True, type=click.BOOL)
def event_loop(is_daemon: bool):
    """
    启动事件循环拉取计划并弹出提醒。
    """
    config = IniFileConfig()
    config.load()
    repository_factory = RepositoryFactory(
        config=config,
    )
    plan_repository = repository_factory.for_plan()
    task_repository = repository_factory.for_task()
    use_case = EventLoopUseCase(
        alerter=Alerter(),
        plan_repository=plan_repository,
        task_repository=task_repository,
    )
    if is_daemon:
        with daemon.DaemonContext():
            use_case.run()
    else:
        use_case.run()
