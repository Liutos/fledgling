# -*- coding: utf8 -*-
from typing import List

from fledgling.app.entity.location import (
    ILocationRepository,
    Location,
)


class ListLocationUseCase:
    def __init__(self, *, location_repository: ILocationRepository):
        self.location_repository = location_repository

    def run(self) -> List[Location]:
        return self.location_repository.find()
