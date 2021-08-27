# -*- coding: utf8 -*-
from datetime import datetime
import json
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
        # TODO: 展示 nest 返回的错误原因。
        if response.status_code != 200:
            raise Exception('登录失败')
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

        started_date_time = datetime.now()
        url = '{}{}'.format(self.url_prefix, pathname)
        try:
            response = request(
                cookies=self.cookies,
                url=url,
                **kwargs
            )
            query_string = []
            for name, value in kwargs.get('params', {}).items():
                query_string.append({
                    'name': name,
                    'value': str(value),
                })
            post_data = {}
            req = response.request
            post_data['mimeType'] = req.headers.get('Content-Type')
            post_data['text'] = req.body
            if isinstance(post_data['text'], bytes):
                post_data['text'] = post_data['text'].decode('utf-8')
            req_cookies = []
            for k, v in self.cookies.items():
                req_cookies.append({
                    'name': k,
                    'value': v,
                })
            req_headers = []
            # TODO: 这种将dict转换为name-value对数组的功能可以提炼一下。
            for k, v in req.headers.items():
                req_headers.append({
                    'name': k,
                    'value': v,
                })
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
                            'status': response.status_code,
                            'statusText': response.raw.reason,
                        },
                        'serverIPAddress': '',
                        'startedDateTime': started_date_time.isoformat(),
                        'time': (datetime.now() - started_date_time).total_seconds(),
                        'timings': {},
                    }],
                    'version': '',
                }
            }))
            return response
        except ConnectionError as e:
            logging.warning('请求{}失败：{}'.format(url, str(e)))
            raise NetworkError()
