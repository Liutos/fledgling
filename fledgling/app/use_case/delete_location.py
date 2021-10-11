# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.app.entity.location import ILocationRepository


class IParams(ABC):
    @abstractmethod
    def get_location_id(self) -> int:
        pass


class DeleteLocationUseCase:
    def __init__(self, *, location_repository: ILocationRepository, params: IParams):
        self.location_repository = location_repository
        self.params = params

    def run(self):
        location_id = self.params.get_location_id()
        self.location_repository.remove(id_=location_id)
