# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class NetworkError(Exception):
    pass


class INestGateway(ABC):
    @abstractmethod
    def login(self, *, email, password):
        pass

    @abstractmethod
    def request(self, *, method: str, pathname: str, skip_login: bool = False, **kwargs):
        """
        向nest服务发送请求。
        """
        pass
