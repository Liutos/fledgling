# -*- coding: utf8 -*-
from fledgling.app.entity.user import (
    IUserRepository,
    User,
    UserRepositoryError,
)
from fledgling.gateway.nest_gateway import INestGateway


class NestUserRepository(IUserRepository):
    def __init__(self, *, nest_client: INestGateway):
        self.nest_client = nest_client

    def save(self, user: User):
        assert user.id is None
        json = {
            'email': user.email,
            'nickname': user.nickname,
            'password': user.password,
        }
        response = self.nest_client.request(
            json=json,
            method='POST',
            pathname='/user',
            skip_login=True,
        )
        response = response.json()
        if response['status'] == 'failure':
            raise UserRepositoryError(response['error']['message'])

        id_ = response['result']['id']
        user.id = id_
