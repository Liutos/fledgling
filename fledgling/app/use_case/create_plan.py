# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, Set, Union

from fledgling.app.entity.plan import IPlanRepository, Plan


class IParams(ABC):
    @abstractmethod
    def get_duration(self) -> Union[None, int]:
        pass

    @abstractmethod
    def get_location_id(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_repeat_interval(self) -> Union[None, timedelta]:
        pass

    @abstractmethod
    def get_repeat_type(self) -> str:
        pass

    @abstractmethod
    def get_task_id(self) -> int:
        pass

    @abstractmethod
    def get_trigger_time(self) -> datetime:
        pass

    @abstractmethod
    def get_visible_hours(self) -> Set[int]:
        pass

    @abstractmethod
    def get_visible_wdays(self) -> Set[int]:
        pass


class CreatePlanUseCase:
    def __init__(self, *, params, plan_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        params = self.params
        duration = params.get_duration()
        location_id = params.get_location_id()
        repeat_interval = params.get_repeat_interval()
        repeat_type = params.get_repeat_type()
        task_id = params.get_task_id()
        trigger_time = params.get_trigger_time()
        visible_hours = params.get_visible_hours()
        visible_wdays = params.get_visible_wdays()
        plan = Plan.new(
            duration=duration,
            location_id=location_id,
            repeat_interval=repeat_interval,
            repeat_type=repeat_type,
            task_id=task_id,
            trigger_time=trigger_time,
            visible_hours=visible_hours,
            visible_wdays=visible_wdays,
        )
        return self.plan_repository.add(plan)
