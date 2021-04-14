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
        if plan.id is None:
            json = {
                'repeat_type': plan.repeat_type,
                'task_id': plan.task_id,
                'trigger_time': plan.trigger_time,
            }
            response = self.nest_client.request(
                json=json,
                method='POST',
                pathname='/plan',
            )
            id_ = response.json()['id']
            plan.id = id_
            return plan
        else:
            json = {
                'repeat_type': plan.repeat_type,
                'trigger_time': plan.trigger_time,
            }
            pathname = '/plan/{}'.format(plan.id)
            self.nest_client.request(
                json=json,
                method='PATCH',
                pathname=pathname,
            )

    def get(self, *, id_):
        pathname = '/plan/{}'.format(id_)
        response = self.nest_client.request(
            method='GET',
            pathname=pathname,
        )
        result = response.json()['result']
        if result is None:
            return None
        # TODO: 统一get/list方法中将HTTP响应结果转换为Plan实例的代码。
        plan = Plan()
        plan.id = result['id']
        plan.task_id = result['task_id']
        plan.trigger_time = result['trigger_time']
        plan.visible_hours = set(result['visible_hours'])
        plan.visible_wdays = set(result['visible_wdays'])
        return plan

    def list(self, *, page, per_page):
        params = {
            'page': page,
            'per_page': per_page,
        }
        response = self.nest_client.request(
            method='GET',
            params=params,
            pathname='/plan',
        )
        plans = response.json()['plans']
        return [Plan.new(
            id_=plan['id'],
            repeat_type=plan['repeat_type'],
            task_id=plan['task_id'],
            trigger_time=plan['trigger_time'],
            visible_hours=set(plan['visible_hours']),
            visible_wdays=set(plan['visible_wdays']),
        ) for plan in plans]

    def pop(self):
        json = {
            'size': 1,
        }
        try:
            response = self.nest_client.request(
                json=json,
                method='POST',
                pathname='/plan/pop',
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
        url = '/plan/{}'.format(id_)
        self.nest_client.request(
            method='DELETE',
            pathname=url,
        )
