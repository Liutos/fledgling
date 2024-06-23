# -*- coding: utf8 -*-
import hashlib
from abc import ABC, abstractmethod
from typing import List

import jieba

from fledgling.app.entity.task import ITaskRepository, Task


class IParams(ABC):
    @abstractmethod
    def get_brief(self) -> str:
        pass

    @abstractmethod
    def get_detail(self) -> str:
        pass

    @abstractmethod
    def get_keywords(self) -> List[str]:
        pass


class CreateTaskUseCase:
    def __init__(self, *, params, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.task_repository = task_repository

    def run(self):
        brief = self.params.get_brief()
        detail = self.params.get_detail()
        keywords = self._gen_keywords()
        task = Task.new(
            brief=brief,
            detail=detail,
            keywords=keywords,
        )
        return self.task_repository.add(task)

    def _gen_keywords(self):
        """生成关键字的哈希值。"""
        brief = self.params.get_brief()
        detail = self.params.get_detail()
        keywords = self.params.get_keywords()
        if not keywords:
            keywords = list(jieba.cut_for_search(brief + ' ' + detail))
            keywords = list(filter(lambda k: k.strip(), keywords))

        result = []
        for keyword in keywords:
            result.append(hashlib.md5(keyword.encode('UTF-8')).hexdigest())

        return result
