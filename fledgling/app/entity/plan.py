# -*- coding: utf8 -*-
from typing import Union

from abc import ABC, abstractmethod


class Plan:
    def __init__(self):
        self.duration = 60
        self.id = None
        self.task_id = None
        self.trigger_time = None

    @classmethod
    def new(cls, *, task_id, trigger_time):
        instance = Plan()
        instance.task_id = task_id
        instance.trigger_time = trigger_time
        return instance


class IPlanRepository(ABC):
    @abstractmethod
    def add(self, plan: Plan) -> Plan:
        """
        将一个计划保存起来。
        """
        pass

    @abstractmethod
    def pop(self) -> Union[None, Plan]:
        """
        获取一个当前能处理的计划，并且之后不再获取到它。
        """
        pass
