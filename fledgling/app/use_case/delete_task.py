# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.app.entity.task import ITaskRepository


class IParams(ABC):
    @abstractmethod
    def get_task_id(self) -> int:
        pass


class DeleteTaskUseCase:
    def __init__(self, *, params, task_repository: ITaskRepository):
        assert isinstance(params, IParams)
        self.params = params
        self.task_repository = task_repository

    def run(self):
        task_id = self.params.get_task_id()
        self.task_repository.remove(task_id=task_id)
