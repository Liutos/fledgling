# -*- coding: utf8 -*-
from typing import List, Optional, Tuple

import click

from fledgling.app.use_case.change_task import ChangeTaskUseCase, IParams
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, task_id: int, *, brief: Optional[str] = None,
                 keywords: Optional[str] = None,
                 status: Optional[int] = None):
        self.brief = brief
        self.keywords = []
        if keywords is not None:
            self.keywords = keywords.split(',')
        self.status = status
        self.task_id = task_id

    def get_brief(self) -> Tuple[bool, Optional[str]]:
        return bool(self.brief), self.brief

    def get_keywords(self) -> Tuple[bool, List[str]]:
        return bool(self.keywords), self.keywords

    def get_status(self) -> Tuple[bool, Optional[int]]:
        return bool(self.status), self.status

    def get_task_id(self) -> int:
        return self.task_id


@click.command()
@click.option('--brief', help='任务简述', type=click.STRING)
@click.option('--keywords', help='关键字', type=click.STRING)
@click.option('--status', help='状态。2 表示已完成，3 表示已取消', type=click.INT)
@click.option('--task-id', help='任务ID', type=click.INT)
@click.pass_context
def change_task(ctx: click.Context, *, brief, keywords, status, task_id):
    """
    修改指定任务。
    """
    params = Params(
        brief=brief,
        keywords=keywords,
        status=status,
        task_id=task_id,
    )
    config = ctx.obj['config']
    repository_factory = RepositoryFactory(config)
    use_case = ChangeTaskUseCase(
        params=params,
        task_repository=repository_factory.for_task(),
    )
    use_case.run()
