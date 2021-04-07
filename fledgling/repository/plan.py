# -*- coding: utf8 -*-
from fledgling.app.entity.plan import IPlanRepository, Plan
from fledgling.repository.nest_gateway import INestGateway


class PlanRepository(IPlanRepository):
    def __init__(self, *, nest_client):
        assert isinstance(nest_client, INestGateway)
        self.nest_client = nest_client

    def add(self, plan: Plan) -> Plan:
        id_ = self.nest_client.plan_create(
            repeat_type=plan.repeat_type,
            task_id=plan.task_id,
            trigger_time=plan.trigger_time,
        )
        plan.id = id_
        return plan

    def list(self, *, page, per_page):
        return self.nest_client.plan_list(
            page=page,
            per_page=per_page,
        )

    def pop(self):
        return self.nest_client.plan_pop()
