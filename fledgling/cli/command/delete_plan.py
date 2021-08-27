# -*- coding: utf8 -*-
import click

from fledgling.app.use_case.delete_plan import DeletePlanUseCase, IParams
from fledgling.cli.repository_factory import RepositoryFactory


class Params(IParams):
    def __init__(self, *, plan_id):
        self.plan_id = plan_id

    def get_plan_id(self) -> int:
        return self.plan_id


@click.command()
@click.option('--plan-id', required=True, type=click.INT)
@click.pass_context
def delete_plan(ctx: click.Context, *, plan_id):
    """
    删除指定计划。
    """
    params = Params(plan_id=plan_id)
    config = ctx.obj['config']
    repository_factory = RepositoryFactory(config)
    use_case = DeletePlanUseCase(
        params=params,
        plan_repository=repository_factory.for_plan(),
    )
    use_case.run()
