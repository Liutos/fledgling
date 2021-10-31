# -*- coding: utf8 -*-
from typing import Optional, Tuple

import click

from fledgling.app.use_case.change_location import ChangeLocationUseCase, IParams
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, location_id: int, *, name: Optional[str] = None):
        self.location_id = location_id
        self.name = name

    def get_location_id(self) -> int:
        return self.location_id

    def get_name(self) -> Tuple[bool, Optional[str]]:
        return bool(self.name), self.name


@click.command()
@click.option('--location-id', help='地点ID', type=click.INT)
@click.option('--name', help='地点名称', type=click.STRING)
@click.pass_context
def change_location(ctx: click.Context, *, location_id, name):
    """
    修改指定地点。
    """
    params = Params(
        location_id=location_id,
        name=name,
    )
    config = ctx.obj['config']
    repository_factory = RepositoryFactory(config)
    use_case = ChangeLocationUseCase(
        location_repository=repository_factory.for_location(),
        params=params,
    )
    use_case.run()
