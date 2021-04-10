# -*- coding: utf8 -*-
import logging

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
        json = {
            'repeat_type': plan.repeat_type,
            'task_id': plan.task_id,
            'trigger_time': plan.trigger_time,
        }
        url = '{}/plan'.format(self.nest_client.url_prefix)
        response = self.nest_client.request(
            json=json,
            method='POST',
            url=url,
        )
        id_ = response.json()['id']
        plan.id = id_
        return plan

    def list(self, *, page, per_page):
        params = {
            'page': page,
            'per_page': per_page,
        }
        url = '{}/plan'.format(self.nest_client.url_prefix)
        response = self.nest_client.request(
            method='GET',
            params=params,
            url=url,
        )
        plans = response.json()['plans']
        return [Plan.new(
            id_=plan['id'],
            repeat_type=plan['repeat_type'],
            task_id=plan['task_id'],
            trigger_time=plan['trigger_time'],
        ) for plan in plans]

    def pop(self):
        url = '{}/plan/pop'.format(self.nest_client.url_prefix)
        json = {
            'size': 1,
        }
        try:
            response = self.nest_client.request(
                json=json,
                method='POST',
                url=url,
            )
        except NetworkError:
            raise PlanRepositoryError()
        print('response.json()', response.json())
        plans = response.json()['plans']
        if len(plans) == 0:
            return None
        return Plan.new(
            task_id=plans[0]['task_id'],
            trigger_time=plans[0]['trigger_time'],
        )

    def remove(self, id_: int):
        url = '{}/plan/{}'.format(self.nest_client.url_prefix, id_)
        self.nest_client.request(
            method='DELETE',
            url=url,
        )
