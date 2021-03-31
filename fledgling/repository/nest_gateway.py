# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class INestGateway(ABC):
    @abstractmethod
    def login(self, *, email, password):
        pass

    @abstractmethod
    def plan_create(self, *, task_id, trigger_time) -> int:
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
