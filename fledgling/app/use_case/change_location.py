# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from fledgling.app.entity.location import ILocationRepository


class LocationNotFoundError(Exception):
    pass


class IParams(ABC):
    @abstractmethod
    def get_name(self) -> Tuple[bool, Optional[str]]:
        pass

    @abstractmethod
    def get_location_id(self) -> int:
        pass


class ChangeLocationUseCase:
    def __init__(self, *, params: IParams, location_repository: ILocationRepository):
        self.params = params
        self.location_repository = location_repository

    def run(self):
        params = self.params
        location = self.location_repository.get(id_=params.get_location_id())
        if location is None:
            raise LocationNotFoundError()

        found, name = params.get_name()
        if found:
            location.brief = name
        self.location_repository.save(location=location)
