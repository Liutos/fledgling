# -*- coding: utf8 -*-
from fledgling.app.entity.plan import IPlanRepository, Plan
from fledgling.repository.nest_gateway import INestGateway


class MockPlanRepository(IPlanRepository):
    def pop(self):
        return Plan(
            duration=300,
            task_id=1,
        )


class PlanRepository(IPlanRepository):
    def __init__(self, *, nest_client):
        assert isinstance(nest_client, INestGateway)
        self.nest_client = nest_client

    def pop(self):
        return self.nest_client.plan_pop()
