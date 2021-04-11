# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Tuple, Union

from fledgling.app.entity.plan import IPlanRepository


class PlanNotFoundError(Exception):
    pass


class IParams(ABC):
    @abstractmethod
    def get_plan_id(self) -> int:
        pass

    @abstractmethod
    def get_repeat_type(self) -> Tuple[bool, Union[None, str]]:
        pass

    @abstractmethod
    def get_trigger_time(self) -> Tuple[bool, Union[None, str]]:
        pass


class ChangePlanUseCase:
    def __init__(self, *, params, plan_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        params = self.params
        plan = self.plan_repository.get(id_=params.get_plan_id())
        if plan is None:
            raise PlanNotFoundError()

        found, repeat_type = params.get_repeat_type()
        if found:
            plan.repeat_type = repeat_type
        found, trigger_time = params.get_trigger_time()
        if found:
            plan.trigger_time = trigger_time

        self.plan_repository.add(plan)
