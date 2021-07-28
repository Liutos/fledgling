# -*- coding: utf8 -*-
from typing import Optional

from PyInquirer import prompt
import click

from fledgling.app.use_case.delete_task import DeleteTaskUseCase, IParams
from fledgling.cli.config import IniFileConfig
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, task_id: Optional[int]):
        self.task_id = task_id

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


@click.command()
@click.option('--task-id', help='要删除的任务的ID', type=click.INT)
def delete_task(*, task_id):
    """
    删除指定任务及其计划。
    """
    params = Params(task_id=task_id)
    config = IniFileConfig()
    config.load()
    repository_factory = RepositoryFactory(config)
    use_case = DeleteTaskUseCase(
        params=params,
        task_repository=repository_factory.for_task(),
    )
    use_case.run()
