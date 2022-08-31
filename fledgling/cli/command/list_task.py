# -*- coding: utf8 -*-
from datetime import datetime
from typing import List, Optional, Tuple
import json

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
    def __init__(self, *, is_json):
        self._is_json = is_json

    def show_task(self, *, tasks: List[Task]):
        if self._is_json:
            click.echo(json.dumps([{
                'brief': task.brief,
                'detail': task.detail,
                'id': task.id,
                'plans': [{
                    'duration': plan.duration,
                    'id': plan.id,
                    'trigger_time': plan.trigger_time.strftime('%Y-%m-%d %H:%M:%S'),
                } for plan in task.plans],
                'status': task.status.value,
            } for task in tasks]))
        else:
            table = []
            for task in tasks:
                status_desc = ''
                if task.is_cancelled():
                    status_desc = '已取消'
                elif task.is_finished():
                    status_desc = '已完成'
                trigger_time_desc = ''
                if len(task.plans) > 0:
                    plan = task.plans[0]
                    trigger_time_desc = self._format_trigger_time(plan.duration, plan.trigger_time)

                table.append([task.id, task.brief, status_desc, trigger_time_desc])
            click.echo(tabulate(
                headers=['任务ID', '任务简述', '状态', '下一次计划的时间'],
                tabular_data=table,
            ))

    # TODO: 消除与文件 fledgling/cli/command/list_plan.py 中的同名方法的重复代码。
    def _format_trigger_time(self, duration: Optional[int], trigger_time: datetime) -> str:
        format_ = '%Y-%m-%d %H:%M:%S'
        now = datetime.now()
        if trigger_time.day == now.day:
            format_ = '%H:%M:%S'
        elif self._is_tomorrow(now, trigger_time):
            format_ = '明天%H:%M:%S'
        elif self._is_day_after_tomorrow(now, trigger_time):
            format_ = '后天%H:%M:%S'
        elif trigger_time.month == now.month:
            format_ = '%d %H:%M:%S'
        elif trigger_time.year == now.year:
            format_ = '%m-%d %H:%M:%S'
        trigger_time_description = trigger_time.strftime(format_)
        if duration is not None and duration > 0:
            trigger_time_description += 'P{}S'.format(duration)
        return trigger_time_description

    def _is_day_after_tomorrow(self, now: datetime, trigger_time: datetime) -> bool:
        return (trigger_time.date() - now.date()).days == 2

    def _is_tomorrow(self, now: datetime, trigger_time: datetime) -> bool:
        return (trigger_time.date() - now.date()).days == 1


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
        presenter=ConsolePresenter(is_json=ctx.obj['is_json']),
        task_repository=repository_factory.for_task(),
    )
    use_case.run()
