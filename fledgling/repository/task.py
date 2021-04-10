# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Union

from fledgling.app.entity.task import (
    ITaskRepository,
    Task,
    TaskRepositoryError,
)
from fledgling.repository.nest_gateway import INestGateway, NetworkError


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
        url = '{}/task'.format(self.nest_client.url_prefix)
        crypted_brief = self.enigma_machine.encrypt(task.brief)
        response = self.nest_client.request(
            json={
                'brief': crypted_brief,
            },
            method='POST',
            url=url,
        )
        id_ = response.json()['id']
        return self.get_by_id(id_)

    def get_by_id(self, id_) -> Union[None, Task]:
        try:
            url = '{}/task/{}'.format(self.nest_client.url_prefix, id_)
            response = self.nest_client.request(
                method='GET',
                url=url,
            )
            task = response.json()['task']
            if not task:
                return None
            brief = self.enigma_machine.decrypt(task['brief'])
            return Task.new(
                brief=brief,
                id_=task['id'],
            )
        except NetworkError:
            raise TaskRepositoryError()

    def list(self, *, page, per_page):
        params = {
            'page': page,
            'per_page': per_page,
        }
        url = '{}/task'.format(self.nest_client.url_prefix)
        response = self.nest_client.request(
            params=params,
            method='GET',
            url=url,
        )
        tasks = response.json()['tasks']
        return [Task.new(
            brief=self.enigma_machine.decrypt(task['brief']),
            id_=task['id'],
        ) for task in tasks]
