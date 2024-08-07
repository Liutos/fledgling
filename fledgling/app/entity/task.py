# -*- coding: utf8 -*-
import typing
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple, Union

from fledgling.app.entity.plan import Plan


class TaskRepositoryError(Exception):
    pass


class TaskStatus(Enum):
    CREATED = 1
    FINISHED = 2
    CANCELLED = 3


class Task:
    def __init__(self):
        self.brief = None
        self.detail: str = ''
        self.id = None
        self.keywords = []
        self.plans: List[Plan] = []
        self.status: Optional[TaskStatus] = None

    @classmethod
    def new(cls, *, brief, detail: str = '', id_=None, keywords: List[str] = None,
            plans: List[Plan] = None,
            status: TaskStatus = None) -> 'Task':
        instance = Task()
        instance.brief = brief
        instance.detail = detail
        instance.id = id_
        instance.keywords = keywords or []
        instance.plans = plans
        instance.status = status
        return instance

    def is_cancelled(self) -> bool:
        return self.status == TaskStatus.CANCELLED

    def is_finished(self) -> bool:
        return self.status == TaskStatus.FINISHED


class ITaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> Task:
        pass

    @abstractmethod
    def get_by_id(self, id_) -> Union[None, Task]:
        """
        查询指定的任务。
        """
        pass

    @abstractmethod
    def list(self, *, keywords: typing.List[str] = None, page, per_page,
             plan_trigger_time: Optional[Tuple[datetime, datetime]] = None,
             status: Optional[int] = None,
             task_ids: Union[None, List[int]] = None):
        """
        列出任务。
        """
        pass

    @abstractmethod
    def remove(self, *, task_id: int):
        pass
