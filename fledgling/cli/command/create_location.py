# -*- coding: utf8 -*-
import click

from fledgling.app.use_case.create_location import CreateLocationUseCase, IParams
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name


@click.command()
@click.option('--name', help='新地点的名称', type=click.STRING)
@click.pass_context
def create_location(ctx: click.Context, name: str):
    """新建一个地点。"""
    config = ctx.obj['config']
    repository_factory = RepositoryFactory(
        config=config,
    )
    use_case = CreateLocationUseCase(
        params=Params(
            name=name,
        ),
        location_repository=repository_factory.for_location(),
    )
    use_case.run()
