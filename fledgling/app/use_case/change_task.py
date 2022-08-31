# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from fledgling.app.entity.task import ITaskRepository, TaskStatus


class TaskNotFoundError(Exception):
    pass


class IParams(ABC):
    @abstractmethod
    def get_brief(self) -> Tuple[bool, Optional[str]]:
        pass

    @abstractmethod
    def get_detail(self) -> Tuple[bool, str]:
        """获取输入的任务详情参数。"""
        pass

    @abstractmethod
    def get_keywords(self) -> Tuple[bool, List[str]]:
        pass

    @abstractmethod
    def get_status(self) -> Tuple[bool, Optional[int]]:
        pass

    @abstractmethod
    def get_task_id(self) -> int:
        pass


class ChangeTaskUseCase:
    def __init__(self, *, params: IParams, task_repository: ITaskRepository):
        self.params = params
        self.task_repository = task_repository

    def run(self):
        params = self.params
        task = self.task_repository.get_by_id(params.get_task_id())
        if task is None:
            raise TaskNotFoundError()

        found, brief = params.get_brief()
        if found:
            task.brief = brief

        found, detail = params.get_detail()
        if found:
            task.detail = detail

        found, keywords = params.get_keywords()
        if found:
            task.keywords = keywords
        found, status = params.get_status()
        if found:
            task.status = TaskStatus(status)
        self.task_repository.add(task)
