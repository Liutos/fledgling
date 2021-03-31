# -*- coding: utf8 -*-
from fledgling.app.use_case.create_plan import CreatePlanUseCase, IParams
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, task_id, trigger_time):
        self.task_id = task_id
        self.trigger_time = trigger_time

    def get_task_id(self) -> int:
        return self.task_id

    def get_trigger_time(self) -> str:
        return self.trigger_time


def create_plan(task_id, trigger_time):
    use_case = CreatePlanUseCase(
        params=Params(
            task_id=task_id,
            trigger_time=trigger_time,
        ),
        plan_repository=RepositoryFactory.for_plan(),
    )
    use_case.run()
