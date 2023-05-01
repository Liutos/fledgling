# -*- coding: utf8 -*-
import abc


class IParams(abc.ABC):
    @abc.abstractmethod
    def get_desp(self) -> str:
        pass

    @abc.abstractmethod
    def get_title(self) -> str:
        pass


class IServerChanService(abc.ABC):
    """实现该接口的类提供了通过 Server 酱 Turbo 版发送消息的能力。"""
    @abc.abstractmethod
    def send(self, *, desp: str = '', title: str):
        """利用 Server 酱 Turbo 版发送消息。"""
        pass


class SendMessageUseCase:
    """通过 Server 酱发送消息给自己的账号或设备。"""
    def __init__(self, *, params: IParams, server_chan_service: IServerChanService):
        self._params = params
        self._server_chan_service = server_chan_service

    def run(self):
        self._server_chan_service.send(
            desp=self._params.get_desp(),
            title=self._params.get_title(),
        )
