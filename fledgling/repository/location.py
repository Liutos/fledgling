# -*- coding: utf8 -*-
from typing import List, Optional, Union

from fledgling.app.entity.location import (
    ILocationRepository,
    Location,
    LocationRepositoryError,
)
from fledgling.gateway.nest_gateway import INestGateway


class NestLocationRepository(ILocationRepository):
    def __init__(self, *, nest_client: INestGateway):
        self.nest_client = nest_client

    def find(self, *, ids: Optional[List[int]] = None, name: Optional[str] = None,
             page: Optional[int] = 1,
             per_page: Optional[int] = 1) -> List[Location]:
        params = {
            'page': page,
            'per_page': per_page,
        }
        if ids is not None:
            params['ids'] = ','.join(map(str, ids))
        if name is not None:
            params['name'] = name

        pathname = '/location'
        response = self.nest_client.request(
            method='GET',
            params=params,
            pathname=pathname,
        )
        response = response.json()
        if response['status'] == 'failure':
            raise LocationRepositoryError(response['error']['message'])

        result = response['result']
        return [self._dto_to_entity(location) for location in result]

    def get(self, *, id_) -> Union[None, Location]:
        pathname = '/location/{}'.format(id_)
        response = self.nest_client.request(
            method='GET',
            pathname=pathname,
        )
        response = response.json()
        if response['status'] == 'failure':
            raise LocationRepositoryError(response['error']['message'])

        result = response['result']
        if result is None:
            return None
        return self._dto_to_entity(result)

    def remove(self, *, id_: int):
        pathname = '/location/{}'.format(id_)
        response = self.nest_client.request(
            method='DELETE',
            pathname=pathname,
        )
        response = response.json()
        if response['status'] == 'failure':
            raise LocationRepositoryError(response['error']['message'])

    def save(self, *, location: Location):
        assert location.id is not None
        pathname = '/location/{}'.format(location.id)
        response = self.nest_client.request(
            method='PATCH',
            pathname=pathname,
        )
        response = response.json()
        if response['status'] == 'failure':
            raise LocationRepositoryError(response['error']['message'])

    def _dto_to_entity(self, dto):
        """将通过网络传输回来的对象反序列化为地点的实体对象。"""
        return Location.new(
            id_=dto['id'],
            name=dto['name'],
            user_id=dto['user_id'],
        )
