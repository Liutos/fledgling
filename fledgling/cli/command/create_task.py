# -*- coding: utf8 -*-
from typing import List
import json

import click
from tabulate import tabulate

from fledgling.app.use_case.create_task import CreateTaskUseCase, IParams
from fledgling.cli.editor import edit_text
from fledgling.cli.repository_factory import RepositoryFactory


# TODO: 最好只需要在该类中定义一次字段，就可以定义出相同的命令行选项。
class Params(IParams):
    def __init__(self, *, brief, detail: str, keywords: str):
        self._detail = detail
        self.brief = brief
        self.keywords = keywords

    def get_brief(self) -> str:
        return self.brief

    def get_detail(self) -> str:
        return self._detail

    def get_keywords(self) -> List[str]:
        keywords = self.keywords.split(',')
        return [keyword for keyword in keywords if len(keyword) > 0]


@click.command()
@click.option('--brief', help='任务简述', required=True, type=str)
@click.option('--detail', default='', help=u'任务详情', type=str)
@click.option('--keywords', default='', help='关键字', type=str)
@click.option('-D', 'from_editor', default=False, help='唤起编辑器来填写任务详情', is_flag=True, show_default=True)
@click.pass_context
def create_task(ctx: click.Context, *, brief, detail: str, from_editor: bool, keywords):
    """
    创建一个任务。
    """
    config = ctx.obj['config']
    is_json: bool = ctx.obj['is_json']
    if from_editor:
        detail = edit_text('')

    params = Params(
        brief=brief,
        detail=detail,
        keywords=keywords,
    )
    repository_factory = RepositoryFactory(
        config=config,
    )
    task_repository = repository_factory.for_task()
    use_case = CreateTaskUseCase(
        params=params,
        task_repository=task_repository,
    )
    task = use_case.run()
    if is_json:
        click.echo(json.dumps({
            'brief': task.brief,
            'detail': task.detail,
            'id': task.id,
        }))
    else:
        click.echo(tabulate(
            headers=['任务ID', '任务简述'],
            tabular_data=[[task.id, task.brief]],
        ))
