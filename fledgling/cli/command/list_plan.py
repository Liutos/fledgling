# -*- coding: utf8 -*-
from fledgling.app.use_case.list_plan import IParams, ListPlanUseCase
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, page, per_page):
        self.page = page
        self.per_page = per_page

    def get_page(self) -> int:
        return self.page

    def get_per_page(self) -> int:
        return self.per_page


class Presenter:
    def __init__(self, plans):
        self.plans = plans

    def format(self):
        for plan in self.plans:
            print('{}\t{}\t{}'.format(plan.id, plan.trigger_time, plan.task.brief))


def list_plan(*, page, per_page):
    """
    列出接下来的计划。
    """
    config = IniFileConfig()
    config.load()
    repository_factory = RepositoryFactory(
        config=config,
    )
    use_case = ListPlanUseCase(
        params=Params(
            page=page,
            per_page=per_page,
        ),
        plan_repository=repository_factory.for_plan(),
        task_repository=repository_factory.for_task(),
    )
    plans = use_case.run()
    presenter = Presenter(plans)
    presenter.format()
