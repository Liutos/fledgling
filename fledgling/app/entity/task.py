# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Union


class Task:
    def __init__(self):
        self.brief = None
        self.id = None

    @classmethod
    def new(cls, *, brief, id_):
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
