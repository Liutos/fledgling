# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from fledgling.app.entity.user import IUserRepository, User


class IParams(ABC):
    @abstractmethod
    def get_email(self) -> str:
        pass

    @abstractmethod
    def get_nickname(self) -> str:
        pass

    @abstractmethod
    def get_password(self) -> str:
        pass


class CreateUserUseCase:
    def __init__(self, *, params: IParams, user_repository: IUserRepository):
        self.params = params
        self.user_repository = user_repository

    def run(self) -> User:
        email = self.params.get_email()
        nickname = self.params.get_nickname()
        password = self.params.get_password()
        user = User(email=email, nickname=nickname, password=password)
        self.user_repository.save(user=user)
        return user
