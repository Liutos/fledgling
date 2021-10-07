# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Union


class PlanRepositoryError(Exception):
    pass


class Plan:
    def __init__(self):
        self.duration = None
        self.id = None
        self.location = None
        self.location_id = None
        self.repeat_interval = None
        self.repeat_type = None
        self.repeating_description: str = ''
        self.task = None
        self.task_id = None
        self.trigger_time: Optional[datetime] = None
        self.visible_hours = set([])
        self.visible_hours_description: str = ''
        self.visible_wdays = set([])
        self.visible_wdays_description: str = ''

    @classmethod
    def new(cls, *, duration: Union[None, int] = None,
            id_=None, location_id: int, repeat_interval: Union[None, timedelta] = None,
            repeat_type=None,
            repeating_description: Union[None, str] = None,
            task_id, trigger_time: datetime, visible_hours=None,
            visible_hours_description: Optional[str] = None,
            visible_wdays=None,
            visible_wdays_description: Optional[str] = None):
        instance = Plan()
        instance.duration = duration
        instance.id = id_
        instance.location_id = location_id
        instance.repeat_interval = repeat_interval
        instance.repeat_type = repeat_type
        instance.repeating_description = repeating_description
        instance.task_id = task_id
        instance.trigger_time = trigger_time
        instance.visible_hours = visible_hours
        instance.visible_hours_description = visible_hours_description
        instance.visible_wdays = visible_wdays
        instance.visible_wdays_description = visible_wdays_description
        return instance

    def is_visible(self, *, trigger_time: datetime):
        """
        判断该计划在给定时刻是否可见。
        """
        if len(self.visible_hours) > 0:
            hour = trigger_time.hour
            if hour not in self.visible_hours:
                return False
        if len(self.visible_wdays) > 0:
            weekday = trigger_time.weekday()
            if weekday not in self.visible_wdays:
                return False
        return True


class IPlanRepository(ABC):
    @abstractmethod
    def add(self, plan: Plan) -> Plan:
        """
        将一个计划保存起来，或更新一个已有的计划。
        """
        pass

    @abstractmethod
    def get(self, *, id_):
        """
        获取指定的计划。
        """
        pass

    @abstractmethod
    def list(self, *, location_id: Optional[int] = None, page, per_page,
             plan_ids: Optional[List[int]] = None) -> Tuple[List[Plan], int]:
        """
        获取指定页码的计划。
        """
        pass

    @abstractmethod
    def pop(self, *, location_id: Optional[int] = None) -> Union[None, Plan]:
        """
        获取一个当前能处理的计划，并且之后不再获取到它。
        """
        pass

    @abstractmethod
    def remove(self, id_: int):
        """
        删除一个指定的计划，之后无法再获取到它。
        """
        pass
