# -*- coding: utf8 -*-
from fledgling.app.use_case.create_task import CreateTaskUseCase, IParams
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, brief):
        self.brief = brief

    def get_brief(self) -> str:
        return self.brief


def create_task(*, brief):
    params = Params(
        brief=brief,
    )
    task_repository = RepositoryFactory.for_task()
    use_case = CreateTaskUseCase(
        params=params,
        task_repository=task_repository,
    )
    use_case.run()
