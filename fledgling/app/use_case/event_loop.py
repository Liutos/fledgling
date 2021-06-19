# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
import logging
import subprocess
import time
from typing import Optional

from fledgling.app.entity.location import ILocationRepository
from fledgling.app.entity.plan import (
    IPlanRepository,
    Plan,
    PlanRepositoryError,
)
from fledgling.app.entity.task import (
    ITaskRepository,
    TaskRepositoryError,
)


_IDLE_SECONDS = 10


class IAlerter(ABC):
    @abstractmethod
    def alert(self, *, plan, task):
        pass


class IParams(ABC):
    @abstractmethod
    def get_location_name(self) -> Optional[str]:
        pass


class AlertState:
    def __init__(self, *, plan: Plan, process: subprocess.Popen):
        self.birth_time = time.time()
        self.plan = plan
        self.process = process

    def is_expired(self):
        now = time.time()
        return isinstance(self.plan.duration, int) and now - self.birth_time > self.plan.duration

    def terminate(self):
        pid = self.process.pid
        try:
            self.process.wait(timeout=1)
            print('进程{}已退出'.format(pid))
        except subprocess.TimeoutExpired:
            self.process.terminate()
            print('向进程{}发送SIGTERM信号'.format(pid))


class InvalidLocationError(Exception):
    def __init__(self, *, name: str):
        self.name = name


class EventLoopUseCase:
    def __init__(self, *, alerter, location_repository: ILocationRepository,
                 params: IParams, plan_repository, task_repository):
        assert isinstance(alerter, IAlerter)
        assert isinstance(plan_repository, IPlanRepository)
        assert isinstance(task_repository, ITaskRepository)
        self.alerter = alerter
        self.alerts = []
        self.location_repository = location_repository
        self.params = params
        self.plan_repository = plan_repository
        self.task_repository = task_repository

    def run(self):
        params = self.params
        location_id = None
        location_name = params.get_location_name()
        if location_name is not None:
            locations = self.location_repository.find(name=location_name)
            if len(locations) == 0:
                raise InvalidLocationError(name=location_name)
            location_id = locations[0].id

        while True:
            try:
                plan = self.plan_repository.pop(location_id=location_id)
                if plan:
                    task_id = plan.task_id
                    task = self.task_repository.get_by_id(task_id)
                    child_process = self.alerter.alert(
                        plan=plan,
                        task=task,
                    )
                    self._keep_child_process(
                        plan=plan,
                        process=child_process,
                    )
                else:
                    print('没有可处理的计划')
            except PlanRepositoryError:
                logging.warning('获取计划失败')
            except TaskRepositoryError:
                logging.warning('获取任务失败')
            self._sort_out_children()
            time.sleep(_IDLE_SECONDS)

    def _keep_child_process(self, *, plan: Plan, process: subprocess.Popen):
        self.alerts.append(AlertState(
            plan=plan,
            process=process,
        ))

    def _sort_out_children(self):
        """
        杀死展示时长已到达上限的进程。
        """
        filtered_alerts = []
        for alert_state in self.alerts:
            if alert_state.is_expired():
                alert_state.terminate()
            else:
                filtered_alerts.append(alert_state)
        self.alerts = filtered_alerts
