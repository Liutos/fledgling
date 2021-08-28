# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple, Union

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
        crypted_brief = self.enigma_machine.encrypt(task.brief)
        response = self.nest_client.request(
            json={
                'brief': crypted_brief,
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

    def list(self, *, keyword: Optional[str] = None, page, per_page,
             plan_trigger_time: Optional[Tuple[datetime, datetime]] = None,
             status: Optional[int] = None,
             task_ids: Union[None, List[int]] = None):
        params = {
            'page': page,
            'per_page': per_page,
        }
        if keyword is not None:
            params['keyword'] = keyword
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
        return Task.new(
            brief=self.enigma_machine.decrypt(dto['brief']),
            id_=dto['id'],
            status=TaskStatus(dto['status']),
        )
