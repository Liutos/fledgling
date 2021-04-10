# -*- coding: utf8 -*-
import click

from fledgling.app.use_case.create_plan import CreatePlanUseCase, IParams
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, repeat_type=None, task_id, trigger_time):
        self.repeat_type = repeat_type
        self.task_id = task_id
        self.trigger_time = trigger_time

    def get_repeat_type(self) -> str:
        return self.repeat_type

    def get_task_id(self) -> int:
        return self.task_id

    def get_trigger_time(self) -> str:
        return self.trigger_time


@click.command()
@click.option('--repeat-type', type=click.STRING)
@click.option('--task-id', required=True, type=click.INT)
@click.option('--trigger-time', required=True, type=str)
def create_plan(repeat_type, task_id, trigger_time):
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
            repeat_type=repeat_type,
            task_id=task_id,
            trigger_time=trigger_time,
        ),
        plan_repository=repository_factory.for_plan(),
    )
    use_case.run()
