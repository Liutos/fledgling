# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Optional


class User:
    def __init__(self, *, email: str, nickname: str, password: str):
        self.email = email
        self.id: Optional[int] = None
        self.nickname = nickname
        self.password = password


class UserRepositoryError(Exception):
    pass


class IUserRepository(ABC):
    @abstractmethod
    def save(self, *, user: User):
        pass
