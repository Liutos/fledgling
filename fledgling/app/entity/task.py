# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List, Optional, Union


class TaskRepositoryError(Exception):
    pass


class Task:
    def __init__(self):
        self.brief = None
        self.id = None

    @classmethod
    def new(cls, *, brief, id_=None):
        instance = Task()
        instance.brief = brief
        instance.id = id_
        return instance


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
             task_ids: Union[None, List[int]] = None):
        """
        列出任务。
        """
        pass
