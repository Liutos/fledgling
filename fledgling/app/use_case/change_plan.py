# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, Set, Tuple, Union

from fledgling.app.entity.plan import IPlanRepository


class PlanNotFoundError(Exception):
    pass


class IParams(ABC):
    @abstractmethod
    def get_duration(self) -> Tuple[bool, Union[None, int]]:
        pass

    @abstractmethod
    def get_location_id(self) -> Tuple[bool, Union[None, int]]:
        pass

    @abstractmethod
    def get_repeat_interval(self) -> Tuple[bool, Union[None, timedelta]]:
        pass

    @abstractmethod
    def get_plan_id(self) -> int:
        pass

    @abstractmethod
    def get_repeat_type(self) -> Tuple[bool, Union[None, str]]:
        pass

    @abstractmethod
    def get_trigger_time(self) -> Tuple[bool, Optional[datetime]]:
        pass

    @abstractmethod
    def get_visible_hours(self) -> Tuple[bool, Union[None, Set[int]]]:
        pass

    @abstractmethod
    def get_visible_wdays(self) -> Tuple[bool, Union[None, Set[int]]]:
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

        found, duration = params.get_duration()
        if found:
            plan.duration = duration
        found, location_id = params.get_location_id()
        if found:
            plan.location_id = location_id
        found, repeat_interval = params.get_repeat_interval()
        if found:
            plan.task_id = repeat_interval
        found, repeat_type = params.get_repeat_type()
        if found:
            plan.repeat_type = repeat_type
        found, trigger_time = params.get_trigger_time()
        if found:
            plan.trigger_time = trigger_time
        found, visible_hours = params.get_visible_hours()
        if found:
            plan.visible_hours = visible_hours
        found, visible_wdays = params.get_visible_wdays()
        if found:
            plan.visible_wdays = visible_wdays

        self.plan_repository.add(plan)
