# -*- coding: utf8 -*-
import click

from fledgling.app.use_case.list_task import IParams, ListTaskUseCase
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


@click.command()
@click.option('--page', default=1, show_default=True)
@click.option('--per-page', default=10, show_default=True)
def list_task(*, page, per_page):
    """
    列出任务。
    """
    params = Params(
        page=page,
        per_page=per_page,
    )
    config = IniFileConfig()
    config.load()
    repository_factory = RepositoryFactory(config)
    use_case = ListTaskUseCase(
        params=params,
        task_repository=repository_factory.for_task(),
    )
    tasks = use_case.run()
    for task in tasks:
        click.echo('{}\t{}'.format(task.id, task.brief))
