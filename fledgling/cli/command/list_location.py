# -*- coding: utf8 -*-
import click
from tabulate import tabulate

from fledgling.app.use_case.list_location import ListLocationUseCase
from fledgling.cli.repository_factory import RepositoryFactory


@click.command()
@click.pass_context
def list_location(ctx: click.Context):
    """列出所有地点。"""
    config = ctx.obj['config']
    repository_factory = RepositoryFactory(
        config=config,
    )
    use_case = ListLocationUseCase(
        location_repository=repository_factory.for_location(),
    )
    locations = use_case.run()
    table = []
    for location in locations:
        table.append([location.id, location.name])
    click.echo(tabulate(
        headers=['地点ID', '名称'],
        tabular_data=table,
    ))
