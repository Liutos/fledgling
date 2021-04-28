# -*- coding: utf8 -*-
import logging
from os.path import isfile
import pickle

from requests import (
    ConnectionError,
    request,
)

from fledgling.repository.nest_gateway import (
    INestGateway,
    NetworkError,
)


class NestClient(INestGateway):
    def __init__(self, *, email: str, cookies_path, hostname, password: str, port, protocol):
        self.cookies_path = cookies_path
        if cookies_path and isfile(cookies_path):
            with open(cookies_path, 'br') as file:
                self.cookies = pickle.load(file)
                print('从文件{}中读入上一次的Cookies'.format(cookies_path))
        else:
            self.cookies = None
        self.email = email
        self.password = password
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
        cookies = response.cookies
        with open(self.cookies_path, 'bw') as file:
            pickle.dump(cookies, file)
            print('将Cookies写入到文件中。')

        self.cookies = cookies

    def request(self, *, pathname, **kwargs):
        if not self.cookies:
            self.login(
                email=self.email,
                password=self.password,
            )

        url = '{}{}'.format(self.url_prefix, pathname)
        try:
            return request(
                cookies=self.cookies,
                url=url,
                **kwargs
            )
        except ConnectionError as e:
            logging.warning('请求{}失败：{}'.format(url, str(e)))
            raise NetworkError()
