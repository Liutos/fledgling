# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class NetworkError(Exception):
    pass


class INestGateway(ABC):
    enigma_machine = None
    url_prefix = None

    @abstractmethod
    def login(self, *, email, password):
        pass

    @abstractmethod
    def request(self, **kwargs):
        """
        向nest服务发送请求。
        """
        pass
