# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Union


class PlanRepositoryError(Exception):
    pass


class Plan:
    def __init__(self):
        self.duration = 60
        self.id = None
        self.repeat_type = None
        self.task = None
        self.task_id = None
        self.trigger_time = None
        self.visible_hours = set([])
        self.visible_wdays = set([])

    @classmethod
    def new(cls, *, id_=None, repeat_type=None, task_id, trigger_time, visible_hours=None, visible_wdays=None):
        instance = Plan()
        instance.id = id_
        instance.repeat_type = repeat_type
        instance.task_id = task_id
        instance.trigger_time = trigger_time
        instance.visible_hours = visible_hours
        instance.visible_wdays = visible_wdays
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
    def list(self, *, page, per_page) -> List[Plan]:
        """
        获取指定页码的计划。
        """
        pass

    @abstractmethod
    def pop(self) -> Union[None, Plan]:
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
