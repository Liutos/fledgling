# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class INestGateway(ABC):
    @abstractmethod
    def login(self, *, email, password):
        pass

    @abstractmethod
    def plan_pop(self):
        pass

    @abstractmethod
    def task_get_by_id(self, id_):
        pass
