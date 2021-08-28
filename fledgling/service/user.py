# -*- coding: utf8 -*-
from fledgling.app.use_case.activate_user import IUserService, UserServiceError
from fledgling.gateway.nest_gateway import INestGateway


class NestUserService(IUserService):
    def __init__(self, *, nest_client: INestGateway):
        self.nest_client = nest_client

    def activate(self, *, activate_code: str, email: str):
        payload = {
            'activate_code': activate_code,
            'email': email,
        }
        pathname = '/user/activation'
        # TODO: 这里封装得不好，让使用者需要查阅 requests 的文档才知道用什么参数。
        response = self.nest_client.request(
            json=payload,
            method='POST',
            pathname=pathname,
            skip_login=True,
        )
        response = response.json()
        if response['status'] == 'failure':
            raise UserServiceError(response['error']['message'])
