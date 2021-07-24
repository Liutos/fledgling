# -*- coding: utf8 -*-
from datetime import datetime
from typing import List, Optional

import click
import colored
from colored import stylize
from wcwidth import wcswidth

from fledgling.app.use_case.list_plan import IParams, ListPlanUseCase
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, location_name: Optional[str], no_location: bool, page, per_page):
        self.location_name = location_name
        self.no_location = no_location
        self.page = page
        self.per_page = per_page

    def get_location_name(self) -> Optional[str]:
        return self.location_name

    def get_no_location(self) -> bool:
        return self.no_location

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
                self._format_trigger_time(plan.duration, plan.trigger_time),
                plan.task.brief,
                plan.repeating_description,
                '是' if plan.is_visible(trigger_time=now) else '否',
                plan.location.name,
                plan.visible_hours_description,
                plan.visible_wdays_description,
            ]
            table.append(row)
        headers = ['计划ID', '计划时间', '任务简述', '重复类型', '是否可见', '地点', '几点可见', '周几可见']
        column_widths = self._compute_column_widths(headers, table)
        separator_row = ['-' * width for width in column_widths]
        self._print_row(column_widths, headers)
        self._print_row(column_widths, separator_row)
        for i, row in enumerate(table):
            if i % 2 == 0:
                styles = [colored.bg('light_gray'), colored.fg('black')]
            else:
                styles = []
            self._print_row(column_widths, row, styles=styles)
        print('共计{}个计划'.format(self.count))

    def _compute_column_widths(self, headers: List[str], table) -> List[int]:
        column_widths = [wcswidth(header) for header in headers]
        for row in table:
            for i in range(0, len(column_widths)):
                v = row[i]
                if not isinstance(v, str):
                    v = str(v)
                length = wcswidth(v)
                if length > column_widths[i]:
                    column_widths[i] = length
        return column_widths

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

    def _print_row(self, column_widths: List[int], row: list, *, styles=None):
        """打印一行。数字为右对齐，其余为左对齐。"""
        columns = []
        for i, value in enumerate(row):
            if isinstance(value, int):
                columns.append('{value:>{width}}'.format(
                    value=value,
                    width=column_widths[i]
                ))
            else:
                # 因为字符串中可能有宽字符，所以需要自己打印右侧的空格。
                length = wcswidth(value)
                columns.append(value + ''.join([' '] * (column_widths[i] - length)))
        row_text = ' ' + '  '.join(columns) + ' '
        if styles:
            row_text = stylize(row_text, styles)
        print(row_text)


@click.command()
@click.option('--no-location', default=False, help='是否不按地点过滤', is_flag=True, show_default=True, type=click.BOOL)
@click.option('--page', default=1, type=click.INT)
@click.option('--per-page', default=10, type=click.INT)
def list_plan(*, no_location: bool, page, per_page):
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
            no_location=no_location,
            page=page,
            per_page=per_page,
        ),
        plan_repository=repository_factory.for_plan(),
        task_repository=repository_factory.for_task(),
    )
    plans, count = use_case.run()
    presenter = Presenter(plans, count)
    presenter.format()
