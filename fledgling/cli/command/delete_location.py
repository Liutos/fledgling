# -*- coding: utf8 -*-
import click

from fledgling.app.entity.location import LocationRepositoryError
from fledgling.app.use_case.delete_location import DeleteLocationUseCase, IParams
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, location_id: int):
        self.location_id = location_id

    def get_location_id(self) -> int:
        return self.location_id


@click.command()
@click.option('--location-id', required=True, type=click.INT)
@click.pass_context
def delete_location(ctx: click.Context, *, location_id: int):
    """删除指定地点。"""
    params = Params(location_id=location_id)
    config = ctx.obj['config']
    repository_factory = RepositoryFactory(config)
    use_case = DeleteLocationUseCase(
        location_repository=repository_factory.for_location(),
        params=params,
    )
    try:
        use_case.run()
    except LocationRepositoryError as e:
        click.echo(str(e))
