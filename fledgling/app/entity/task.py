# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple, Union


class TaskRepositoryError(Exception):
    pass


class TaskStatus(Enum):
    CREATED = 1
    FINISHED = 2
    CANCELLED = 3


class Task:
    def __init__(self):
        self.brief = None
        self.id = None
        self.keywords = []
        self.status: Optional[TaskStatus] = None

    @classmethod
    def new(cls, *, brief, id_=None, keywords: List[str] = None,
            status: TaskStatus = None) -> 'Task':
        instance = Task()
        instance.brief = brief
        instance.id = id_
        instance.keywords = keywords or []
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
    def list(self, *, keyword: Optional[str] = None, page, per_page,
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
