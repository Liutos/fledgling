# -*- coding: utf8 -*-
import hashlib
import typing
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple

import jieba

from fledgling.app.entity.task import ITaskRepository, Task


class IParams(ABC):
    def get_keyword_hashes(self) -> typing.List[str]:
        """获取关键字分词后的哈希值。"""
        result = []
        keyword = self.get_keyword()
        if not keyword:
            return result

        parts = jieba.cut_for_search(keyword)
        for part in parts:
            result.append(hashlib.md5(part.encode('UTF-8')).hexdigest())

        return result

    @abstractmethod
    def get_keyword(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_page(self) -> int:
        pass

    @abstractmethod
    def get_per_page(self) -> int:
        pass

    def get_plan_trigger_time(self) -> Optional[Tuple[datetime, datetime]]:
        raise NotImplementedError

    def get_status(self) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    def get_task_ids(self) -> Optional[List[int]]:
        pass


class IPresenter(ABC):
    def show_task(self, *, tasks: List[Task]):
        raise NotImplementedError


class ListTaskUseCase:
    def __init__(self, *, params, presenter: IPresenter, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.presenter = presenter
        self.task_repository = task_repository

    def run(self):
        params = self.params
        hashes = params.get_keyword_hashes()
        page = params.get_page()
        per_page = params.get_per_page()
        task_ids = params.get_task_ids()
        tasks = self.task_repository.list(
            keywords=hashes,
            page=page,
            per_page=per_page,
            plan_trigger_time=params.get_plan_trigger_time(),
            status=params.get_status(),
            task_ids=task_ids,
        )
        self.presenter.show_task(tasks=tasks)
