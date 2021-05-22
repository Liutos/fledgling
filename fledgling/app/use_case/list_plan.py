# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.app.entity.location import ILocationRepository
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
    def __init__(self, *, location_repository: ILocationRepository,
                 params, plan_repository, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        assert isinstance(task_repository, ITaskRepository)
        self.location_repository = location_repository
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
        task_ids = [plan.task_id for plan in plans]
        tasks = self.task_repository.list(
            page=1,
            per_page=len(task_ids),
            task_ids=task_ids,
        )
        for plan in plans:
            location_id = plan.location_id
            location = self.location_repository.get(id_=location_id)
            plan.location = location
            task_id = plan.task_id
            task = [task for task in tasks if task.id == task_id][0]
            plan.task = task

        return plans
