# -*- coding: utf8 -*-
import click
from datetime import timedelta
from typing import List, Set, Union

from fledgling.app.use_case.create_plan import CreatePlanUseCase, IParams
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


# TODO: 这里的参数其实依赖于click.option，不够内聚。最好让这个Params类自己负责解析命令行参数。
class Params(IParams):
    def __init__(self, *, duration: Union[None, int] = None,
                 repeat_interval: Union[None, int] = None,
                 repeat_type=None, task_id, trigger_time,
                 visible_hours: Union[None, List[int]] = None,
                 visible_wdays: Union[None, List[int]] = None):
        self.duration = duration
        self.repeat_interval = repeat_interval
        self.repeat_type = repeat_type
        self.task_id = task_id
        self.trigger_time = trigger_time
        self.visible_hours = set(visible_hours or [])
        self.visible_wdays = set(visible_wdays or [])

    def get_duration(self) -> Union[None, int]:
        return self.duration

    def get_repeat_interval(self) -> Union[None, timedelta]:
        return isinstance(self.repeat_interval, int) and timedelta(seconds=self.repeat_interval)

    def get_repeat_type(self) -> str:
        return self.repeat_type

    def get_task_id(self) -> int:
        return self.task_id

    def get_trigger_time(self) -> str:
        return self.trigger_time

    def get_visible_hours(self) -> Set[int]:
        return self.visible_hours

    def get_visible_wdays(self) -> Set[int]:
        return self.visible_wdays


def validate_visible_hours(ctx, param, value: Union[None, str]):
    if value is None:
        return None

    return map(int, value.split(','))


@click.command()
@click.option('--duration', type=click.INT)
@click.option('--repeat-interval', type=click.INT)
@click.option('--repeat-type', type=click.STRING)
@click.option('--task-id', required=True, type=click.INT)
@click.option('--trigger-time', required=True, type=str)
@click.option('--visible-hours', callback=validate_visible_hours, type=click.STRING)
@click.option('--visible-wdays', callback=validate_visible_hours, type=click.STRING)
def create_plan(duration,
                repeat_interval, repeat_type, task_id, trigger_time, visible_hours, visible_wdays):
    """
    为任务创建一个计划。
    """
    config = IniFileConfig()
    config.load()
    repository_factory = RepositoryFactory(
        config=config,
    )
    use_case = CreatePlanUseCase(
        params=Params(
            duration=duration,
            repeat_interval=repeat_interval,
            repeat_type=repeat_type,
            task_id=task_id,
            trigger_time=trigger_time,
            visible_hours=visible_hours,
            visible_wdays=visible_wdays,
        ),
        plan_repository=repository_factory.for_plan(),
    )
    use_case.run()
