# -*- coding: utf8 -*-
from fledgling.app.use_case.event_loop import EventLoopUseCase
from fledgling.cli.alerter import Alerter
from fledgling.cli.repository_factory import RepositoryFactory


def event_loop():
    plan_repository = RepositoryFactory.for_plan()
    task_repository = RepositoryFactory.for_task()
    use_case = EventLoopUseCase(
        alerter=Alerter(),
        plan_repository=plan_repository,
        task_repository=task_repository,
    )
    use_case.run()

