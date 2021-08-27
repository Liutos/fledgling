# -*- coding: utf8 -*-
from typing import Optional

from PyInquirer import prompt
from tabulate import tabulate
import click

from fledgling.app.entity.task import Task
from fledgling.app.use_case.delete_task import DeleteTaskUseCase, IParams, IPresenter
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, task_id: Optional[int]):
        self.task_id = task_id

    def get_confirmation(self) -> bool:
        if self.task_id:
            return True
        questions = [
            {
                'message': '确定删除该任务',
                'name': 'confirmation',
                'type': 'confirm',
            }
        ]
        answers = prompt(questions)
        return answers['confirmation']

    def get_task_id(self) -> int:
        if self.task_id:
            return self.task_id
        questions = [
            {
                'message': '输入要删除的任务的ID',
                'name': 'task_id',
                'type': 'input',
            }
        ]
        answers = prompt(questions)
        return answers['task_id']


class ConsolePresenter(IPresenter):
    def show_task(self, *, task: Task):
        table = [[str(task.id), task.brief, '是' if task.is_finished() else '否']]
        click.echo(tabulate(
            headers=['任务ID', '任务简述', '是否已完成'],
            tabular_data=table,
        ))


@click.command()
@click.option('--task-id', help='要删除的任务的ID', type=click.INT)
@click.pass_context
def delete_task(ctx: click.Context, *, task_id):
    """
    删除指定任务及其计划。
    """
    params = Params(task_id=task_id)
    config = ctx.obj['config']
    repository_factory = RepositoryFactory(config)
    use_case = DeleteTaskUseCase(
        params=params,
        presenter=ConsolePresenter(),
        task_repository=repository_factory.for_task(),
    )
    use_case.run()
