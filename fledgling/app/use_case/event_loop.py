# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
import logging
import subprocess
import time

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


class AlertState:
    def __init__(self, *, plan: Plan, process: subprocess.Popen):
        self.birth_time = time.time()
        self.plan = plan
        self.process = process

    def is_expired(self):
        now = time.time()
        return now - self.birth_time > self.plan.duration

    def terminate(self):
        pid = self.process.pid
        print('杀死进程{}'.format(pid))
        self.process.terminate()


class EventLoopUseCase:
    def __init__(self, *, alerter, plan_repository, task_repository):
        assert isinstance(alerter, IAlerter)
        assert isinstance(plan_repository, IPlanRepository)
        assert isinstance(task_repository, ITaskRepository)
        self.alerter = alerter
        self.alerts = []
        self.plan_repository = plan_repository
        self.task_repository = task_repository

    def run(self):
        while True:
            try:
                plan = self.plan_repository.pop()
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
