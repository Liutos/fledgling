# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class IParams(ABC):
    @abstractmethod
    def get_activate_code(self) -> str:
        pass

    @abstractmethod
    def get_email(self) -> str:
        pass


class UserServiceError(Exception):
    pass


class IUserService(ABC):
    @abstractmethod
    def activate(self, *, activate_code: str, email: str):
        pass


class ActivateUserUseCase:
    def __init__(self, *, params: IParams, user_service: IUserService):
        self.params = params
        self.user_service = user_service

    def run(self):
        activate_code = self.params.get_activate_code()
        email = self.params.get_email()
        self.user_service.activate(activate_code=activate_code, email=email)
