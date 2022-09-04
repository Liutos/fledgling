# -*- coding: utf8 -*-
from typing import List, Optional, Tuple

import click

from fledgling.app.use_case.change_task import ChangeTaskUseCase, IParams
from fledgling.cli import (
    editor,
    setting,
)
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, task_id: int, *, brief: Optional[str] = None,
                 detail: Optional[str] = None,
                 from_editor: bool = False,
                 keywords: Optional[str] = None,
                 status: Optional[str] = None):
        """参数 editor 如果为 True，则会调起编辑器用于修改任务的详情。"""
        self._from_editor = from_editor
        self.brief = brief
        self.detail = detail
        self.keywords = []
        if keywords is not None:
            self.keywords = keywords.split(',')
        self.status = None
        if status is not None:
            self.status = int(status)
        self.task_id = task_id

    def get_brief(self) -> Tuple[bool, Optional[str]]:
        return bool(self.brief), self.brief

    def get_detail(self, detail: str) -> Tuple[bool, str]:
        if self.detail != '':
            return True, self.detail
        elif self._from_editor:
            return True, editor.edit_text(detail)
        else:
            return False, ''

    def get_keywords(self) -> Tuple[bool, List[str]]:
        return bool(self.keywords), self.keywords

    def get_status(self) -> Tuple[bool, Optional[int]]:
        return bool(self.status), self.status

    def get_task_id(self) -> int:
        return self.task_id


@click.command()
@click.option('--brief', help='任务简述', type=click.STRING)
@click.option('--detail', default='', help=u'任务详情', type=str)
@click.option('--keywords', help='关键字', type=click.STRING)
@click.option('--status', help=setting.STATUS_HELP, type=click.Choice(setting.STATUS))
@click.option('--task-id', help='任务ID', type=click.INT)
@click.option('-D', 'from_editor', default=False, help='唤起编辑器来填写任务详情', is_flag=True, show_default=True)
@click.pass_context
def change_task(ctx: click.Context, *, brief, detail: str, from_editor: bool, keywords, status: str, task_id):
    """
    修改指定任务。
    """
    params = Params(
        brief=brief,
        detail=detail,
        from_editor=from_editor,
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
