# -*- coding: utf8 -*-
from datetime import datetime
import json
import logging
from os.path import isfile
from typing import Optional
import pickle

from requests import (
    ConnectionError,
    PreparedRequest,
    Response,
    request,
)

from fledgling.gateway.nest_gateway import (
    INestGateway,
    NetworkError,
)


class NestClient(INestGateway):
    def __init__(self, *, email: str, cookies_path, hostname, password: str, port, protocol):
        self.cookies_path = cookies_path
        if cookies_path and isfile(cookies_path):
            with open(cookies_path, 'br') as file:
                self.cookies = pickle.load(file)
        else:
            self.cookies = None
        self.email = email
        self.password = password
        self.url_prefix = '{}://{}:{}'.format(protocol, hostname, port)

    def login(self, *, email, password):
        response = self.request(
            json={
                'email': email,
                'password': password,
            },
            method='POST',
            pathname='/user/login',
            skip_login=True,
        )
        if response.status_code != 200:
            # 这里遇到了一个用 HTTP 状态码来承载业务处理结果的坏处：即使已知响应的状态码不为 200，却仍然无法假定此时 response.text 中的
            # 数据的格式。
            decoded = json.loads(response.text)
            error = decoded['error']
            raise Exception('登录失败：{}, {}'.format(error['code'], error['message']))

        cookies = response.cookies
        with open(self.cookies_path, 'bw') as file:
            pickle.dump(cookies, file)

        self.cookies = cookies

    # TODO: 建议分化出一个 authenticated_request，避免该方法与 login 递归。
    def request(self, *, pathname, skip_login: bool = False, **kwargs):
        if not skip_login and not self.cookies:
            self.login(
                email=self.email,
                password=self.password,
            )

        started_date_time = datetime.now()
        url = '{}{}'.format(self.url_prefix, pathname)
        # 必须在此定义，否则 finally 中将有可能是未定义的变量。
        req: Optional[PreparedRequest] = None
        response: Optional[Response] = None
        try:
            response = request(
                cookies=self.cookies,
                url=url,
                **kwargs
            )
            req = response.request

            return response
        except ConnectionError as e:
            logging.warning('请求{}失败：{}'.format(url, str(e)))
            raise NetworkError()
        finally:
            req_cookies = []
            if self.cookies is not None:
                req_cookies = self._extract_name_values(self.cookies)

            post_data = {}
            req_headers = []
            if req is not None:
                req_headers = self._extract_name_values(req.headers)

                post_data = {
                    'mimeType': req.headers.get('Content-Type'),
                    'text': req.body,
                }
                if isinstance(post_data['text'], bytes):
                    post_data['text'] = post_data['text'].decode('utf-8')

            query_string = self._extract_name_values(kwargs.get('params', {}))

            content = {}
            if response is not None:
                content = {
                    'mimeType': response.headers['Content-Type'],
                    'size': response.headers['Content-Length'],
                    'text': response.text,
                }

            logging.debug(json.dumps({
                'log': {
                    'creator': {
                        'name': 'fledgling',
                    },
                    'entries': [{
                        'cache': {},
                        'request': {
                            'bodySize': 0,
                            'cookies': req_cookies,
                            'headers': req_headers,
                            'headersSize': 0,
                            'httpVersion': '',
                            'method': kwargs['method'],
                            'postData': post_data,
                            'queryString': query_string,
                            'url': url,
                        },
                        'response': {
                            'bodySize': 0,
                            'content': content,
                            'cookies': [],
                            'headers': {},
                            'headersSize': 0,
                            'httpVersion': '',
                            'redirectUrl': '',
                            'status': response and response.status_code,
                            'statusText': response and response.raw.reason,
                        },
                        'serverIPAddress': '',
                        'startedDateTime': started_date_time.isoformat(),
                        'time': (datetime.now() - started_date_time).total_seconds(),
                        'timings': {},
                    }],
                    'version': '',
                }
            }))

    def _extract_name_values(self, dct):
        if dct is None:
            return []

        name_values = []
        for name, value in dct.items():
            name_values.append({
                'name': name,
                'value': str(value),
            })

        return name_values
