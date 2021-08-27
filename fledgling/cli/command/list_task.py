# -*- coding: utf8 -*-
from datetime import datetime
from typing import List, Optional, Tuple

import click
from tabulate import tabulate

from fledgling.app.entity.task import Task
from fledgling.app.use_case.list_task import IParams, IPresenter, ListTaskUseCase
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, keyword: Optional[str] = None, page, per_page,
                 plan_trigger_time: Optional[str],
                 status: Optional[int]):
        self.keyword = keyword
        self.page = page
        self.per_page = per_page
        self.plan_trigger_time = None
        self.status = status
        if plan_trigger_time:
            begin, end = plan_trigger_time.split(',')
            self.plan_trigger_time = (
                datetime.strptime(begin, '%Y-%m-%d %H:%M:%S'),
                datetime.strptime(end, '%Y-%m-%d %H:%M:%S'),
            )

    def get_keyword(self) -> Optional[str]:
        return self.keyword

    def get_page(self) -> int:
        return self.page

    def get_per_page(self) -> int:
        return self.per_page

    def get_plan_trigger_time(self) -> Optional[Tuple[datetime, datetime]]:
        return self.plan_trigger_time

    def get_status(self) -> Optional[int]:
        return self.status


class ConsolePresenter(IPresenter):
    def show_task(self, *, tasks: List[Task]):
        table = []
        for task in tasks:
            table.append([task.id, task.brief, '是' if task.is_finished() else '否'])
        click.echo(tabulate(
            headers=['任务ID', '任务简述', '是否已完成'],
            tabular_data=table,
        ))


@click.command()
@click.option('--keyword', help='过滤任务的关键字')
@click.option('--page', default=1, show_default=True)
@click.option('--per-page', default=10, show_default=True)
@click.option('--plan-trigger-time', help='任务的计划触发时间范围', type=str)
@click.option('--status', help='任务的状态', type=click.INT)
@click.pass_context
def list_task(ctx: click.Context, *, keyword, page, per_page, plan_trigger_time, status):
    """
    列出任务。
    """
    params = Params(
        keyword=keyword,
        page=page,
        per_page=per_page,
        plan_trigger_time=plan_trigger_time,
        status=status,
    )
    config = ctx.obj['config']
    repository_factory = RepositoryFactory(config)
    use_case = ListTaskUseCase(
        params=params,
        presenter=ConsolePresenter(),
        task_repository=repository_factory.for_task(),
    )
    use_case.run()
