# -*- coding: utf8 -*-
from typing import Set, Tuple, Union

from fledgling.app.use_case.change_plan import (
    ChangePlanUseCase,
    IParams,
)
from fledgling.repository.nest_gateway import INestGateway
from fledgling.repository.plan import PlanRepository

_repeat_type = None


class MockResponse:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


class MockNestClient(INestGateway):
    def login(self, *, email, password):
        pass

    def request(self, *, pathname, **kwargs):
        method = kwargs['method']
        if method == 'GET':
            return MockResponse({
                'result': {
                    'duration': 0,
                    'id': 233,
                    'repeat_type': 'hourly',
                    'task_id': 634,
                    'trigger_time': '2021-04-21 23:19:00',
                    'visible_hours': [],
                    'visible_wdays': [],
                },
                'status': 'success',
            })
        else:
            json_data = kwargs['json']
            global _repeat_type
            _repeat_type = json_data['repeat_type']
            return MockResponse({
                'status': 'success',
            })


class MockParams(IParams):
    def get_duration(self) -> Tuple[bool, Union[None, int]]:
        return True, 60

    def get_plan_id(self) -> int:
        return 233

    def get_repeat_type(self) -> Tuple[bool, Union[None, str]]:
        return False, None

    def get_trigger_time(self) -> Tuple[bool, Union[None, str]]:
        return False, None

    def get_visible_hours(self) -> Tuple[bool, Union[None, Set[int]]]:
        return False, None

    def get_visible_wdays(self) -> Tuple[bool, Union[None, Set[int]]]:
        return False, None


def test_without_repeat_type():
    """
    测试更新计划时没有传入repeat_type的情况。
    """
    use_case = ChangePlanUseCase(
        params=MockParams(),
        plan_repository=PlanRepository(
            nest_client=MockNestClient(),
        )
    )
    use_case.run()
    assert _repeat_type == 'hourly'
