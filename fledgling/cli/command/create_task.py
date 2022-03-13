# -*- coding: utf8 -*-
from typing import List
import json

import click
from tabulate import tabulate

from fledgling.app.use_case.create_task import CreateTaskUseCase, IParams
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, brief, keywords: str):
        self.brief = brief
        self.keywords = keywords

    def get_brief(self) -> str:
        return self.brief

    def get_keywords(self) -> List[str]:
        keywords = self.keywords.split(',')
        return [keyword for keyword in keywords if len(keyword) > 0]


@click.command()
@click.option('--brief', help='任务简述', required=True, type=str)
@click.option('--keywords', default='', help='关键字', type=str)
@click.pass_context
def create_task(ctx: click.Context, *, brief, keywords):
    """
    创建一个任务。
    """
    config = ctx.obj['config']
    is_json: bool = ctx.obj['is_json']
    params = Params(
        brief=brief,
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
            'id': task.id,
        }))
    else:
        click.echo(tabulate(
            headers=['任务ID', '任务简述'],
            tabular_data=[[task.id, task.brief]],
        ))
