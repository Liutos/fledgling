# -*- coding: utf8 -*-
from typing import Union

from fledgling.app.entity.task import ITaskRepository, Task
from fledgling.repository.nest_gateway import INestGateway


class MockTaskRepository(ITaskRepository):
    def get_by_id(self, id_) -> Union[None, Task]:
        return Task.new(
            brief='Hello, world!',
            id_=id_,
        )


class TaskRepository(ITaskRepository):
    def __init__(self, *, nest_client):
        assert isinstance(nest_client, INestGateway)
        self.nest_client = nest_client

    def get_by_id(self, id_) -> Union[None, Task]:
        return self.nest_client.task_get_by_id(id_)
