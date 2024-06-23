# -*- coding: utf8 -*-
import typing
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Union

from fledgling.app.entity.plan import Plan
from fledgling.app.entity.task import (
    ITaskRepository,
    Task,
    TaskRepositoryError,
    TaskStatus,
)
from fledgling.gateway.nest_gateway import INestGateway, NetworkError


class IEnigmaMachine(ABC):
    @abstractmethod
    def decrypt(self, cipher_text):
        pass

    @abstractmethod
    def encrypt(self, plain_text):
        pass


class TaskRepository(ITaskRepository):
    def __init__(self, *, enigma_machine, nest_client):
        assert isinstance(enigma_machine, IEnigmaMachine)
        assert isinstance(nest_client, INestGateway)
        self.enigma_machine = enigma_machine
        self.nest_client = nest_client

    def add(self, task: Task) -> Task:
        encrypted_detail = self.enigma_machine.encrypt(task.detail)
        if task.id is None:
            crypted_brief = self.enigma_machine.encrypt(task.brief)
            response = self.nest_client.request(
                json={
                    'brief': crypted_brief,
                    'detail': encrypted_detail,
                    'keywords': task.keywords,
                },
                method='POST',
                pathname='/task',
            )
            response = response.json()
            if response['status'] == 'failure':
                raise TaskRepositoryError(response['error']['message'])

            id_ = response['result']['id']
            return self.get_by_id(id_)
        else:
            crypted_brief = self.enigma_machine.encrypt(task.brief)
            response = self.nest_client.request(
                json={
                    'brief': crypted_brief,
                    'detail': encrypted_detail,
                    'keywords': task.keywords,
                    'status': task.status.value,
                },
                method='PATCH',
                pathname='/task/{}'.format(task.id),
            )
            response = response.json()
            if response['status'] == 'failure':
                raise TaskRepositoryError(response['error']['message'])

            id_ = response['result']['id']
            return self.get_by_id(id_)

    def get_by_id(self, id_) -> Union[None, Task]:
        try:
            pathname = '/task/{}'.format(id_)
            response = self.nest_client.request(
                method='GET',
                pathname=pathname,
            )
            response = response.json()
            if response['status'] == 'failure':
                raise TaskRepositoryError(response['error']['message'])

            task = response['result']
            if not task:
                return None
            return self._dto_to_entity(task)
        except NetworkError:
            raise TaskRepositoryError()

    def list(self, *, keywords: typing.List[str] = None, page, per_page,
             plan_trigger_time: Optional[Tuple[datetime, datetime]] = None,
             status: Optional[int] = None,
             task_ids: Union[None, List[int]] = None):
        params = {
            'page': page,
            'per_page': per_page,
        }
        if keywords is not None:
            params['keywords'] = keywords

        if plan_trigger_time:
            params['plan_trigger_time'] = ','.join([
                plan_trigger_time[0].strftime('%Y-%m-%d %H:%M:%S'),
                plan_trigger_time[1].strftime('%Y-%m-%d %H:%M:%S'),
            ])
        if status:
            params['status'] = status
        if task_ids is not None:
            params['task_ids'] = ','.join([str(task_id) for task_id in task_ids])

        response = self.nest_client.request(
            params=params,
            method='GET',
            pathname='/task',
        )
        response = response.json()
        if response['status'] == 'failure':
            raise TaskRepositoryError(response['error']['message'])

        tasks = response['result']
        return [self._dto_to_entity(task) for task in tasks]

    def remove(self, *, task_id: int):
        response = self.nest_client.request(
            method='DELETE',
            pathname='/task/{}'.format(task_id),
        )
        response = response.json()
        if response['status'] == 'failure':
            raise TaskRepositoryError(response['error']['message'])

    def _dto_to_entity(self, dto: dict):
        plans = []
        for plan_dto in dto['plans']:
            plans.append(self._plan_dto_to_entity(plan_dto))

        detail = ''
        if dto['detail'] is not None:
            detail = self.enigma_machine.decrypt(dto['detail'])

        return Task.new(
            brief=self.enigma_machine.decrypt(dto['brief']),
            detail=detail,
            id_=dto['id'],
            plans=plans,
            status=TaskStatus(dto['status']),
        )

    # TODO: 消除与文件 fledgling/repository/plan.py 中方法 _dto_to_entity 的重复代码。
    def _plan_dto_to_entity(self, dto: dict) -> Plan:
        """将计划的 DTO 转换为实体对象。"""
        plan = Plan()
        plan.duration = dto['duration']
        plan.id = dto['id']
        plan.location_id = dto['location_id']
        if isinstance(dto.get('repeat_interval'), int):
            plan.repeat_interval = timedelta(seconds=dto.get('repeat_interval'))
        plan.repeat_type = dto['repeat_type']
        plan.repeating_description = dto['repeating_description']
        plan.task_id = dto['task_id']
        plan.trigger_time = datetime.strptime(dto['trigger_time'], '%Y-%m-%d %H:%M:%S')
        plan.visible_hours = set(dto['visible_hours'])
        plan.visible_hours_description = dto['visible_hours_description']
        plan.visible_wdays = set(dto['visible_wdays'])
        plan.visible_wdays_description = dto['visible_wdays_description']
        return plan
