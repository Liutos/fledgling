# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Union


class Location:
    def __init__(self):
        self.id = None
        self.name = None
        self.user_id = None

    @classmethod
    def new(cls, *, id_: int = None, name: str, user_id: int):
        instance = Location()
        instance.id = id_
        instance.name = name
        instance.user_id = user_id
        return instance


class ILocationRepository(ABC):
    @abstractmethod
    def get(self, *, id_: int) -> Union[None, Location]:
        pass


class LocationRepositoryError(Exception):
    pass
