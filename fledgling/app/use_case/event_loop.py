# -*- coding: utf8 -*-
import typing
from abc import ABC, abstractmethod
import datetime
import logging
import subprocess
import time
from typing import Optional

from fledgling.app.entity.location import ILocationRepository, InvalidLocationError
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


class IDoNotDisturbService(ABC):
    """提供与勿扰模式有关的服务。"""
    @abstractmethod
    def check_do_not_disturb(self, begin_time: datetime.time, end_time: datetime.time,
                             *, now: datetime.datetime = None) -> bool:
        """如果当前时间落在了用户设置的勿扰时段内，就返回 True，否则返回 False。"""
        pass

    @abstractmethod
    def check_do_not_disturb_with_reason(self, begin_time: datetime.time, end_time: datetime.time,
                                         *, now: datetime.datetime = None) -> typing.Tuple[bool, str]:
        """如果当前时间落在了用户设置的勿扰时段内，就返回 True，否则返回 False。"""
        pass


class IParams(ABC):
    @abstractmethod
    def get_do_not_disturb_begin_time(self) -> Optional[datetime.time]:
        """获得勿扰模式的开始时间。"""
        pass

    @abstractmethod
    def get_do_not_disturb_end_time(self) -> Optional[datetime.time]:
        """获得勿扰模式的结束时间。如果该方法的返回值早于方法 get_do_not_disturb_begin_time 的返回值，那么它表示的是明天的同一时刻。"""
        pass

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
            logging.info('进程{}已退出'.format(pid))
        except subprocess.TimeoutExpired:
            self.process.terminate()
            logging.info('向进程{}发送SIGTERM信号'.format(pid))


class EventLoopUseCase:
    def __init__(self, *, alerter, location_repository: ILocationRepository,
                 do_not_disturb_service: IDoNotDisturbService,
                 params: IParams, plan_repository, task_repository):
        assert isinstance(alerter, IAlerter)
        assert isinstance(plan_repository, IPlanRepository)
        assert isinstance(task_repository, ITaskRepository)
        self._do_not_disturb_service = do_not_disturb_service
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
        if location_name:
            locations = self.location_repository.find(name=location_name)
            if len(locations) == 0:
                raise InvalidLocationError(name=location_name)
            location_id = locations[0].id

        while True:
            try:
                do_not_disturb, reason = self._check_do_not_disturb()
                logging.info('_check_do_not_disturb 检查结果：%s' % reason)
                if do_not_disturb:
                    plan = None
                else:
                    plan = self.plan_repository.pop(location_id=location_id)

                if plan:
                    if plan.is_outdated(datetime.datetime.now()):
                        logging.info('计划{}已经过期了。trigger_time={}，duration={}'.format(
                            plan.id,
                            plan.trigger_time.strftime('%Y-%m-%d %H:%M:%S'),
                            plan.duration,
                        ))
                    else:
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
                    logging.info('没有可处理的计划')
            except PlanRepositoryError:
                logging.warning('获取计划失败')
            except TaskRepositoryError:
                logging.warning('获取任务失败')
            self._sort_out_children()
            time.sleep(_IDLE_SECONDS)

    def _check_do_not_disturb(self) -> typing.Tuple[bool, str]:
        """检查当前是否在勿扰的时间段内。"""
        begin_time = self.params.get_do_not_disturb_begin_time()
        if begin_time is None:
            return False, '起点时间为空'

        end_time = self.params.get_do_not_disturb_end_time()
        if end_time is None:
            return False, '终点时间为空'

        return self._do_not_disturb_service.check_do_not_disturb_with_reason(begin_time, end_time)

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
