# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.app.entity.location import (
    ILocationRepository,
    Location,
)


class IParams(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass


class LocationNameInUsedError(Exception):
    def __init__(self, *, name: str):
        self.name = name


class CreateLocationUseCase:
    def __init__(self, *, location_repository: ILocationRepository, params: IParams):
        self.params = params
        self.location_repository = location_repository

    # 用例负责维护与repository有关的业务逻辑，例如不允许创建重名的地点。
    def run(self):
        params = self.params
        name = params.get_name()
        existing = self.location_repository.find(name=name)
        if len(existing) > 0:
            raise LocationNameInUsedError(name=name)

        location = Location.new(
            name=name,
        )
        return self.location_repository.save(location=location)
