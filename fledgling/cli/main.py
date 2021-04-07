# -*- coding: utf8 -*-
import click

from fledgling.cli.command.create_config import create_config
from fledgling.cli.command.create_plan import create_plan
from fledgling.cli.command.create_task import create_task
from fledgling.cli.command.event_loop import event_loop
from fledgling.cli.command.list_plan import list_plan
from fledgling.cli.command.list_task import list_task

cli = click.Group()

create_config_command = click.Command(
    'create-config',
    callback=create_config,
    params=[
        click.Option(
            default=False,
            param_decls=['--overwrite'],
            show_default=True,
            type=click.BOOL,
        ),
    ],
    short_help=create_config.__doc__,
)
cli.add_command(create_config_command)

create_plan_command = click.Command(
    'create-plan',
    callback=create_plan,
    params=[
        click.Option(
            param_decls=['--repeat-type'],
            required=False,
            type=click.STRING,
        ),
        click.Option(
            param_decls=['--task-id'],
            required=True,
            type=click.INT,
        ),
        click.Option(
            param_decls=['--trigger-time'],
            required=True,
            type=str,
        )
    ],
    short_help=create_plan.__doc__,
)
cli.add_command(create_plan_command)

create_task_command = click.Command(
    'create-task',
    callback=create_task,
    params=[
        click.Option(
            param_decls=['--brief'],
            required=True,
            type=str,
        )
    ],
    short_help=create_task.__doc__,
)
cli.add_command(create_task_command)

event_loop_command = click.Command(
    'event-loop',
    callback=event_loop,
    params=[
        click.Option(
            default=False,
            param_decls=['--is-daemon'],
            required=False,
            type=click.BOOL,
        ),
    ],
    short_help=event_loop.__doc__,
)
cli.add_command(event_loop_command)

list_plan_command = click.Command(
    'list-plan',
    callback=list_plan,
    params=[
        click.Option(
            default=1,
            param_decls=['--page'],
            required=False,
            type=click.INT,
        ),
        click.Option(
            default=10,
            param_decls=['--per-page'],
            required=False,
            type=click.INT,
        ),
    ],
    short_help=list_plan.__doc__,
)
cli.add_command(list_plan_command)

cli.add_command(list_task)


if __name__ == '__main__':
    cli()
