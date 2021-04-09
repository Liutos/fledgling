# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class NetworkError(Exception):
    pass


class INestGateway(ABC):
    @abstractmethod
    def login(self, *, email, password):
        pass

    @abstractmethod
    def plan_create(self, *, repeat_type=None, task_id, trigger_time) -> int:
        pass

    @abstractmethod
    def plan_delete(self, *, plan_id):
        pass

    @abstractmethod
    def plan_list(self, *, page, per_page):
        pass

    @abstractmethod
    def plan_pop(self):
        pass

    @abstractmethod
    def task_create(self, *, brief):
        pass

    @abstractmethod
    def task_get_by_id(self, id_):
        pass

    @abstractmethod
    def task_list(self, *, page, per_page):
        pass
