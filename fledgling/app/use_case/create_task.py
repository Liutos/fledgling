# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List

from fledgling.app.entity.task import ITaskRepository, Task


class IParams(ABC):
    @abstractmethod
    def get_brief(self) -> str:
        pass

    @abstractmethod
    def get_keywords(self) -> List[str]:
        pass


class CreateTaskUseCase:
    def __init__(self, *, params, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.task_repository = task_repository

    def run(self):
        brief = self.params.get_brief()
        task = Task.new(
            brief=brief,
            keywords=self.params.get_keywords(),
        )
        return self.task_repository.add(task)
