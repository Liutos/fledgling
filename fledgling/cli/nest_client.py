# -*- coding: utf8 -*-
import logging

from requests import (
    ConnectionError,
    request,
)

from fledgling.repository.nest_gateway import (
    INestGateway,
    NetworkError,
)


class NestClient(INestGateway):
    def __init__(self, *, hostname, port, protocol):
        self.cookies = None
        self.url_prefix = '{}://{}:{}'.format(protocol, hostname, port)

    def login(self, *, email, password):
        response = request(
            json={
                'email': email,
                'password': password,
            },
            method='POST',
            url='{}/user/login'.format(self.url_prefix),
        )
        self.cookies = response.cookies

    def request(self, *, pathname, **kwargs):
        try:
            return request(
                cookies=self.cookies,
                url='{}{}'.format(self.url_prefix, pathname),
                **kwargs
            )
        except ConnectionError as e:
            logging.warning('请求{}失败：{}'.format(kwargs['url'], str(e)))
            raise NetworkError()
