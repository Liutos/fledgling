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
                 status: Optional[int],
                 task_ids_text: Optional[str] = None):
        self.keyword = keyword
        self.page = page
        self.per_page = per_page
        self.plan_trigger_time = None
        self.status = status
        self.task_ids = None
        if plan_trigger_time:
            begin, end = plan_trigger_time.split(',')
            self.plan_trigger_time = (
                datetime.strptime(begin, '%Y-%m-%d %H:%M:%S'),
                datetime.strptime(end, '%Y-%m-%d %H:%M:%S'),
            )
        if task_ids_text:
            self.task_ids = [int(task_id) for task_id in task_ids_text.split(',')]

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

    def get_task_ids(self) -> Optional[List[int]]:
        return self.task_ids


class ConsolePresenter(IPresenter):
    def show_task(self, *, tasks: List[Task]):
        table = []
        for task in tasks:
            status_desc = ''
            if task.is_cancelled():
                status_desc = '已取消'
            elif task.is_finished():
                status_desc = '已完成'
            table.append([task.id, task.brief, status_desc])
        click.echo(tabulate(
            headers=['任务ID', '任务简述', '状态'],
            tabular_data=table,
        ))


@click.command()
@click.option('--keyword', help='过滤任务的关键字')
@click.option('--page', default=1, show_default=True)
@click.option('--per-page', default=10, show_default=True)
@click.option('--plan-trigger-time', help='任务的计划触发时间范围', type=str)
@click.option('--status', help='任务的状态', type=click.INT)
@click.option('--task-ids', help='要查看的任务的ID', type=str)
@click.pass_context
def list_task(ctx: click.Context, *, keyword, page, per_page, plan_trigger_time, status, task_ids):
    """
    列出任务。
    """
    params = Params(
        keyword=keyword,
        page=page,
        per_page=per_page,
        plan_trigger_time=plan_trigger_time,
        status=status,
        task_ids_text=task_ids,
    )
    config = ctx.obj['config']
    repository_factory = RepositoryFactory(config)
    use_case = ListTaskUseCase(
        params=params,
        presenter=ConsolePresenter(),
        task_repository=repository_factory.for_task(),
    )
    use_case.run()
