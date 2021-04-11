# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class NetworkError(Exception):
    pass


class INestGateway(ABC):
    @abstractmethod
    def login(self, *, email, password):
        pass

    @abstractmethod
    def request(self, *, pathname, **kwargs):
        """
        向nest服务发送请求。
        """
        pass
