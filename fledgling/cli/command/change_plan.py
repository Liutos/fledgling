# -*- coding: utf8 -*-
from typing import Tuple, Union

import click

from fledgling.app.use_case.change_plan import ChangePlanUseCase, IParams
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, plan_id, repeat_type, trigger_time):
        self.plan_id = plan_id
        self.repeat_type = repeat_type
        self.trigger_time = trigger_time

    def get_plan_id(self) -> int:
        return self.plan_id

    def get_repeat_type(self) -> Tuple[bool, Union[None, str]]:
        return bool(self.repeat_type), self.repeat_type

    def get_trigger_time(self) -> Tuple[bool, Union[None, str]]:
        return bool(self.trigger_time), self.trigger_time


@click.command()
@click.option('--plan-id', required=True, type=click.INT)
@click.option('--repeat-type', type=click.STRING)
@click.option('--trigger-time', type=click.STRING)
def change_plan(*, plan_id, repeat_type, trigger_time):
    """
    修改指定计划。
    """
    params = Params(
        plan_id=plan_id,
        repeat_type=repeat_type,
        trigger_time=trigger_time
    )
    config = IniFileConfig()
    config.load()
    repository_factory = RepositoryFactory(config)
    use_case = ChangePlanUseCase(
        params=params,
        plan_repository=repository_factory.for_plan(),
    )
    use_case.run()
