# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.app.entity.plan import IPlanRepository
from fledgling.app.entity.task import ITaskRepository


class IParams(ABC):
    @abstractmethod
    def get_page(self) -> int:
        pass

    @abstractmethod
    def get_per_page(self) -> int:
        pass


class ListPlanUseCase:
    def __init__(self, *, params, plan_repository, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.plan_repository = plan_repository
        self.task_repository = task_repository

    def run(self):
        page = self.params.get_page()
        per_page = self.params.get_per_page()
        plans = self.plan_repository.list(
            page=page,
            per_page=per_page,
        )
        for plan in plans:
            task_id = plan.task_id
            task = self.task_repository.get_by_id(task_id)
            plan.task = task

        return plans
