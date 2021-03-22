# -*- coding: utf8 -*-
from typing import Union

from abc import ABC, abstractmethod


class Plan:
    def __init__(self, *, duration, task_id):
        self.duration = duration
        self.task_id = task_id


class IPlanRepository(ABC):
    @abstractmethod
    def pop(self) -> Union[None, Plan]:
        """
        获取一个当前能处理的计划，并且之后不再获取到它。
        """
        pass
