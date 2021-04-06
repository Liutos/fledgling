# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List

from fledgling.app.entity.task import ITaskRepository, Task


class IParams(ABC):
    @abstractmethod
    def get_page(self) -> int:
        pass

    @abstractmethod
    def get_per_page(self) -> int:
        pass


class ListTaskUseCase:
    def __init__(self, *, params, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.task_repository = task_repository

    def run(self) -> List[Task]:
        params = self.params
        page = params.get_page()
        per_page = params.get_per_page()
        return self.task_repository.list(
            page=page,
            per_page=per_page,
        )
