# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.app.entity.plan import IPlanRepository, Plan


class IParams(ABC):
    @abstractmethod
    def get_repeat_type(self) -> str:
        pass

    @abstractmethod
    def get_task_id(self) -> int:
        pass

    @abstractmethod
    def get_trigger_time(self) -> str:
        pass


class CreatePlanUseCase:
    def __init__(self, *, params, plan_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        params = self.params
        repeat_type = params.get_repeat_type()
        task_id = params.get_task_id()
        trigger_time = params.get_trigger_time()
        plan = Plan.new(
            repeat_type=repeat_type,
            task_id=task_id,
            trigger_time=trigger_time,
        )
        return self.plan_repository.add(plan)
