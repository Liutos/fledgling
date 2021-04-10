# -*- coding: utf8 -*-
from typing import Union

from fledgling.app.entity.task import (
    ITaskRepository,
    Task,
    TaskRepositoryError,
)
from fledgling.repository.nest_gateway import INestGateway, NetworkError


class TaskRepository(ITaskRepository):
    def __init__(self, *, nest_client):
        assert isinstance(nest_client, INestGateway)
        self.nest_client = nest_client

    def add(self, task: Task) -> Task:
        id_ = self.nest_client.task_create(
            brief=task.brief,
        )
        return self.get_by_id(id_)

    def get_by_id(self, id_) -> Union[None, Task]:
        try:
            return self.nest_client.task_get_by_id(id_)
        except NetworkError:
            raise TaskRepositoryError()

    def list(self, *, page, per_page):
        return self.nest_client.task_list(
            page=page,
            per_page=per_page,
        )
