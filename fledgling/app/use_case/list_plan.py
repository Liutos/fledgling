# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Optional

from fledgling.app.entity.location import ILocationRepository, InvalidLocationError
from fledgling.app.entity.plan import IPlanRepository
from fledgling.app.entity.task import ITaskRepository


class IParams(ABC):
    def get_location_name(self) -> Optional[str]:
        raise NotImplementedError

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
        location_id = None
        location_name = self.params.get_location_name()
        if location_name is not None:
            locations = self.location_repository.find(name=location_name)
            if len(locations) == 0:
                raise InvalidLocationError(name=location_name)
            location_id = locations[0].id

        page = self.params.get_page()
        per_page = self.params.get_per_page()
        criteria = {
            'page': page,
            'per_page': per_page,
        }
        if location_id is not None:
            criteria['location_id'] = location_id
        plans, count = self.plan_repository.list(**criteria)
        location_ids = [plan.location_id for plan in plans]
        locations = self.location_repository.find(
            ids=location_ids,
            page=1,
            per_page=len(location_ids),
        )
        task_ids = [plan.task_id for plan in plans]
        tasks = self.task_repository.list(
            page=1,
            per_page=len(task_ids),
            task_ids=task_ids,
        )
        for plan in plans:
            location_id = plan.location_id
            location = [location for location in locations if location.id == location_id][0]
            plan.location = location
            task_id = plan.task_id
            task = [task for task in tasks if task.id == task_id][0]
            plan.task = task

        return plans, count
