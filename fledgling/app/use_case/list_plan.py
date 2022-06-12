# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List, Optional

from fledgling.app.entity.location import (
    ILocationRepository,
    InvalidLocationError,
    Location,
)
from fledgling.app.entity.plan import IPlanRepository, Plan
from fledgling.app.entity.task import ITaskRepository, Task


class IParams(ABC):
    def get_location_name(self) -> Optional[str]:
        raise NotImplementedError

    def get_no_location(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_page(self) -> int:
        pass

    @abstractmethod
    def get_per_page(self) -> int:
        pass

    @abstractmethod
    def get_plan_ids(self) -> Optional[List[int]]:
        pass

    @abstractmethod
    def get_task_ids(self) -> List[int]:
        pass


class IPresenter(ABC):
    @abstractmethod
    def on_find_location(self):
        pass

    @abstractmethod
    def on_find_task(self):
        pass

    @abstractmethod
    def on_invalid_location(self, *, error: InvalidLocationError):
        pass

    @abstractmethod
    def show_plans(self, *, count: int, plans: List[Plan]):
        pass


class ListPlanUseCase:
    def __init__(self, *, location_repository: ILocationRepository,
                 params, plan_repository,
                 presenter: IPresenter,
                 task_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        assert isinstance(task_repository, ITaskRepository)
        self.location_repository = location_repository
        self.params = params
        self.plan_repository = plan_repository
        self.presenter = presenter
        self.task_repository = task_repository

    def run(self):
        location_id = None
        location_name = self.params.get_location_name()
        no_location = self.params.get_no_location()
        if not no_location and location_name is not None:
            locations = self.location_repository.find(name=location_name)
            if len(locations) == 0:
                self.presenter.on_invalid_location(error=InvalidLocationError(name=location_name))
                return

            location_id = locations[0].id

        page = self.params.get_page()
        per_page = self.params.get_per_page()
        criteria = {
            'page': page,
            'per_page': per_page,
        }
        if location_id is not None:
            criteria['location_id'] = location_id
        plan_ids = self.params.get_plan_ids()
        if plan_ids is not None:
            criteria['plan_ids'] = plan_ids
        criteria['task_ids'] = self.params.get_task_ids()
        # 如果指定了要查看的计划或者计划所属的任务的 ID，那么就不应当继续用 location 的 ID 来过滤。
        if (plan_ids is not None or len(criteria['task_ids']) > 0) and 'location_id' in criteria:
            del criteria['location_id']

        plans, count = self.plan_repository.list(**criteria)
        self.presenter.on_find_location()
        locations = self._find_locations(plans)
        self.presenter.on_find_task()
        tasks = self._find_tasks(plans)
        for plan in plans:
            location_id = plan.location_id
            location = [location for location in locations if location.id == location_id][0]
            plan.location = location
            task_id = plan.task_id
            task = [task for task in tasks if task.id == task_id][0]
            plan.task = task

        self.presenter.show_plans(
            count=count,
            plans=plans,
        )
        return

    def _find_locations(self, plans: List[Plan]) -> List[Location]:
        if len(plans) == 0:
            return []

        location_ids = [plan.location_id for plan in plans]
        return self.location_repository.find(
            ids=location_ids,
            page=1,
            per_page=len(location_ids),
        )

    def _find_tasks(self, plans: List[Plan]) -> List[Task]:
        if len(plans) == 0:
            return []

        task_ids = [plan.task_id for plan in plans]
        return self.task_repository.list(
            page=1,
            per_page=len(task_ids),
            task_ids=task_ids,
        )
