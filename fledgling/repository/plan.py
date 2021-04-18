# -*- coding: utf8 -*-
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
                'duration': plan.duration,
                'repeat_type': plan.repeat_type,
                'task_id': plan.task_id,
                'trigger_time': plan.trigger_time,
                'visible_hours': list(plan.visible_hours),
                'visible_wdays': list(plan.visible_wdays),
            }
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
            json = {
                'duration': plan.duration,
                'repeat_type': plan.repeat_type,
                'trigger_time': plan.trigger_time,
                'visible_hours': list(plan.visible_hours),
                'visible_wdays': list(plan.visible_wdays),
            }
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
        # TODO: 统一get/list方法中将HTTP响应结果转换为Plan实例的代码。
        plan = Plan()
        plan.duration = result['duration']
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
        response = response.json()
        if response['status'] == 'failure':
            raise PlanRepositoryError(response['error']['message'])

        plans = response['result']
        return [Plan.new(
            duration=plan['duration'],
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
        response = response.json()
        if response['status'] == 'failure':
            raise PlanRepositoryError(response['error']['message'])

        print('response', response)
        plans = response['result']
        if len(plans) == 0:
            return None
        return Plan.new(
            duration=plans[0]['duration'],
            task_id=plans[0]['task_id'],
            trigger_time=plans[0]['trigger_time'],
        )

    def remove(self, id_: int):
        url = '/plan/{}'.format(id_)
        response = self.nest_client.request(
            method='DELETE',
            pathname=url,
        )
        response = response.json()
        if response['status'] == 'failure':
            raise PlanRepositoryError(response['error']['message'])
