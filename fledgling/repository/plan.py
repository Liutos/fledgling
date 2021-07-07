# -*- coding: utf8 -*-
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Union

from fledgling.app.entity.plan import (
    IPlanRepository,
    Plan,
    PlanRepositoryError,
)
from fledgling.repository.nest_gateway import INestGateway, NetworkError


class PlanRepository(IPlanRepository):
    def __init__(self, *, nest_client):
        assert isinstance(nest_client, INestGateway)
        self.nest_client = nest_client

    def add(self, plan: Plan) -> Plan:
        if plan.id is None:
            json = self._entity_to_dto(plan)
            json['task_id'] = plan.task_id
            response = self.nest_client.request(
                json=json,
                method='POST',
                pathname='/plan',
            )
            response = response.json()
            if response['status'] == 'failure':
                raise PlanRepositoryError(response['error']['message'])

            id_ = response['result']['id']
            plan.id = id_
            return plan
        else:
            json = self._entity_to_dto(plan)
            print('json', json)
            pathname = '/plan/{}'.format(plan.id)
            response = self.nest_client.request(
                json=json,
                method='PATCH',
                pathname=pathname,
            )
            # TODO: 统一到处一样的异常处理代码
            response = response.json()
            if response['status'] == 'failure':
                raise PlanRepositoryError(response['error']['message'])

    def get(self, *, id_):
        pathname = '/plan/{}'.format(id_)
        response = self.nest_client.request(
            method='GET',
            pathname=pathname,
        )
        response = response.json()
        if response['status'] == 'failure':
            raise PlanRepositoryError(response['error']['message'])

        result = response['result']
        if result is None:
            return None
        return self._dto_to_entity(result)

    def list(self, *, page, per_page) -> Tuple[List[Plan], int]:
        params = {
            'page': page,
            'per_page': per_page,
        }
        response = self.nest_client.request(
            method='GET',
            params=params,
            pathname='/plan',
        )
        response = response.json()
        if response['status'] == 'failure':
            raise PlanRepositoryError(response['error']['message'])

        count = response['result']['count']
        plans = response['result']['plans']
        return [self._dto_to_entity(plan) for plan in plans], count

    def pop(self, *, location_id: Optional[int] = None):
        json = {
            'size': 1,
        }
        if location_id:
            json['location_id'] = location_id
        try:
            response = self.nest_client.request(
                json=json,
                method='POST',
                pathname='/plan/pop',
            )
        except NetworkError:
            raise PlanRepositoryError()
        response = response.json()
        if response['status'] == 'failure':
            raise PlanRepositoryError(response['error']['message'])

        print('response', response)
        plans = response['result']
        if len(plans) == 0:
            return None
        return self._dto_to_entity(plans[0])

    def remove(self, id_: int):
        url = '/plan/{}'.format(id_)
        response = self.nest_client.request(
            method='DELETE',
            pathname=url,
        )
        response = response.json()
        if response['status'] == 'failure':
            raise PlanRepositoryError(response['error']['message'])

    def _dto_to_entity(self, dto: dict) -> Plan:
        plan = Plan()
        plan.duration = dto['duration']
        plan.id = dto['id']
        plan.location_id = dto['location_id']
        if isinstance(dto.get('repeat_interval'), int):
            plan.repeat_interval = timedelta(seconds=dto.get('repeat_interval'))
        plan.repeat_type = dto['repeat_type']
        plan.repeating_description = dto['repeating_description']
        plan.task_id = dto['task_id']
        plan.trigger_time = datetime.strptime(dto['trigger_time'], '%Y-%m-%d %H:%M:%S')
        plan.visible_hours = set(dto['visible_hours'])
        plan.visible_hours_description = dto['visible_hours_description']
        plan.visible_wdays = set(dto['visible_wdays'])
        plan.visible_wdays_description = dto['visible_wdays_description']
        return plan

    def _entity_to_dto(self, plan: Plan) -> dict:
        repeat_interval: Union[None, timedelta] = plan.repeat_interval
        seconds = None
        if repeat_interval is not None:
            seconds = int(repeat_interval.total_seconds())
        return {
            'duration': plan.duration,
            'location_id': plan.location_id,
            'repeat_interval': seconds,
            'repeat_type': plan.repeat_type,
            'trigger_time': plan.trigger_time.strftime('%Y-%m-%d %H:%M:%S'),
            'visible_hours': list(plan.visible_hours),
            'visible_wdays': list(plan.visible_wdays),
        }
