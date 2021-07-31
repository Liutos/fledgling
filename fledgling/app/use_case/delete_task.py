# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.app.entity.task import ITaskRepository, Task


class IParams(ABC):
    @abstractmethod
    def get_confirmation(self) -> bool:
        """获取用户是否要删除该任务的确认。"""
        pass

    @abstractmethod
    def get_task_id(self) -> int:
        pass


class IPresenter(ABC):
    @abstractmethod
    def show_task(self, *, task: Task):
        pass


class DeleteTaskUseCase:
    def __init__(self, *, params, presenter: IPresenter, task_repository: ITaskRepository):
        assert isinstance(params, IParams)
        self.params = params
        self.presenter = presenter
        self.task_repository = task_repository

    def run(self):
        task_id = self.params.get_task_id()
        task = self.task_repository.get_by_id(task_id)
        self.presenter.show_task(task=task)
        is_confirmed = self.params.get_confirmation()
        if is_confirmed:
            self.task_repository.remove(task_id=task_id)
