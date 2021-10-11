# -*- coding: utf8 -*-
from typing import List, Optional, Union
import unittest

from fledgling.app.entity.location import (
    ILocationRepository,
    Location,
)
from fledgling.app.use_case.delete_location import (
    DeleteLocationUseCase,
    IParams,
)


class MockLocationRepository(ILocationRepository):
    def __init__(self):
        self.location_id = None

    def get(self, *, id_: int) -> Union[None, Location]:
        pass

    def find(self, *, ids: Optional[List[int]] = None,
             name: Optional[str] = None,
             page: Optional[int] = 1,
             per_page: Optional[int] = 1) -> List[Location]:
        pass

    def remove(self, *, id_: int):
        self.location_id = id_


class MockParams(IParams):
    def get_location_id(self) -> int:
        return 233


class DeleteLocationTestCase(unittest.TestCase):
    def test_delete_location(self):
        """测试删除地点时传递的参数"""
        repository = MockLocationRepository()
        use_case = DeleteLocationUseCase(
            location_repository=repository,
            params=MockParams(),
        )
        use_case.run()
        self.assertEqual(repository.location_id, 233)
