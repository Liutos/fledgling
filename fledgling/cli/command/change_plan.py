# -*- coding: utf8 -*-
from typing import List, Set, Tuple, Union

import click

from fledgling.app.use_case.change_plan import ChangePlanUseCase, IParams
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, plan_id, repeat_type, trigger_time,
                 visible_hours: Union[None, List[int]] = None,
                 visible_wdays: Union[None, List[int]] = None):
        self.plan_id = plan_id
        self.repeat_type = repeat_type
        self.trigger_time = trigger_time
        self.visible_hours = set(visible_hours or [])
        self.visible_wdays = set(visible_wdays or [])

    def get_plan_id(self) -> int:
        return self.plan_id

    def get_repeat_type(self) -> Tuple[bool, Union[None, str]]:
        return bool(self.repeat_type), self.repeat_type

    def get_trigger_time(self) -> Tuple[bool, Union[None, str]]:
        return bool(self.trigger_time), self.trigger_time

    def get_visible_hours(self) -> Tuple[bool, Union[None, Set[int]]]:
        return bool(self.visible_hours), self.visible_hours

    def get_visible_wdays(self) -> Tuple[bool, Union[None, Set[int]]]:
        return bool(self.visible_wdays), self.visible_wdays


def validate_visible_hours(ctx, param, value: Union[None, str]):
    if value is None:
        return None

    return map(int, value.split(','))


@click.command()
@click.option('--plan-id', required=True, type=click.INT)
@click.option('--repeat-type', type=click.STRING)
@click.option('--trigger-time', type=click.STRING)
@click.option('--visible-hours', callback=validate_visible_hours, type=click.STRING)
@click.option('--visible-wdays', callback=validate_visible_hours, type=click.STRING)
def change_plan(*, plan_id, repeat_type, trigger_time, visible_hours, visible_wdays):
    """
    修改指定计划。
    """
    params = Params(
        plan_id=plan_id,
        repeat_type=repeat_type,
        trigger_time=trigger_time,
        visible_hours=visible_hours,
        visible_wdays=visible_wdays,
    )
    config = IniFileConfig()
    config.load()
    repository_factory = RepositoryFactory(config)
    use_case = ChangePlanUseCase(
        params=params,
        plan_repository=repository_factory.for_plan(),
    )
    use_case.run()