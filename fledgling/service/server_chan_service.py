# -*- coding: utf8 -*-
import requests

from fledgling.app.use_case.send_message import IServerChanService


class ServerChanServiceConfig:
    def __init__(self, send_key: str):
        self.send_key = send_key


class ServerChanService(IServerChanService):
    def __init__(self, config: ServerChanServiceConfig):
        self._config = config

    def send(self, *, desp: str = '', title: str):
        # server 酱的接口文档：https://sct.ftqq.com/sendkey
        url = 'https://sctapi.ftqq.com/{}.send'.format(self._config.send_key)
        data = {
            'desp': desp,
            'title': title[:32],  # server 酱的 title 的最大长度为 32。
        }
        requests.post(url, data=data)
