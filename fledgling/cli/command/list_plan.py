# -*- coding: utf8 -*-
import click
from datetime import datetime
from tabulate import tabulate

from fledgling.app.use_case.list_plan import IParams, ListPlanUseCase
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, page, per_page):
        self.page = page
        self.per_page = per_page

    def get_page(self) -> int:
        return self.page

    def get_per_page(self) -> int:
        return self.per_page


class Presenter:
    def __init__(self, plans):
        self.plans = plans

    def format(self):
        table = []
        now = datetime.now()
        for plan in self.plans:
            row = [
                plan.id,
                plan.trigger_time,
                plan.task.brief,
                plan.repeat_type,
                '是' if plan.is_visible(trigger_time=now) else '否',
                plan.duration if isinstance(plan.duration, int) and plan.duration > 0 else '-',
            ]
            table.append(row)
        print(tabulate(
            headers=['计划ID', '计划时间', '任务简述', '重复类型', '是否可见', '展示时长'],
            tabular_data=table,
        ))


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
        params=Params(
            page=page,
            per_page=per_page,
        ),
        plan_repository=repository_factory.for_plan(),
        task_repository=repository_factory.for_task(),
    )
    plans = use_case.run()
    presenter = Presenter(plans)
    presenter.format()
