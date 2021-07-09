# -*- coding: utf8 -*-
from typing import Optional

import click
from datetime import datetime
from tabulate import tabulate

from fledgling.app.use_case.list_plan import IParams, ListPlanUseCase
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, location_name: Optional[str], page, per_page):
        self.location_name = location_name
        self.page = page
        self.per_page = per_page

    def get_location_name(self) -> Optional[str]:
        return self.location_name

    def get_page(self) -> int:
        return self.page

    def get_per_page(self) -> int:
        return self.per_page


class Presenter:
    def __init__(self, plans, count: int):
        self.count = count
        self.plans = plans

    def format(self):
        table = []
        now = datetime.now()
        for plan in self.plans:
            row = [
                plan.id,
                self._format_trigger_time(plan.trigger_time),
                plan.task.brief,
                plan.repeating_description,
                '是' if plan.is_visible(trigger_time=now) else '否',
                plan.duration if isinstance(plan.duration, int) and plan.duration > 0 else '-',
                plan.location.name,
                plan.visible_hours_description,
                plan.visible_wdays_description,
            ]
            table.append(row)
        print(tabulate(
            headers=['计划ID', '计划时间', '任务简述', '重复类型', '是否可见', '展示时长', '地点', '几点可见', '周几可见'],
            tabular_data=table,
        ))
        print('共计{}个计划'.format(self.count))

    def _format_trigger_time(self, trigger_time: datetime) -> str:
        now = datetime.now()
        if trigger_time.day == now.day:
            return trigger_time.strftime('%H:%M:%S')
        if trigger_time.month == now.month:
            return trigger_time.strftime('%d %H:%M:%S')
        if trigger_time.year == now.year:
            return trigger_time.strftime('%m-%d %H:%M:%S')
        return trigger_time.strftime('%Y-%m-%d %H:%M:%S')


@click.command()
@click.option('--page', default=1, type=click.INT)
@click.option('--per-page', default=10, type=click.INT)
def list_plan(*, page, per_page):
    """
    列出接下来的计划。
    """
    config = IniFileConfig()
    config.load()
    repository_factory = RepositoryFactory(
        config=config,
    )
    use_case = ListPlanUseCase(
        location_repository=repository_factory.for_location(),
        params=Params(
            location_name=config['location']['name'],
            page=page,
            per_page=per_page,
        ),
        plan_repository=repository_factory.for_plan(),
        task_repository=repository_factory.for_task(),
    )
    plans, count = use_case.run()
    presenter = Presenter(plans, count)
    presenter.format()
