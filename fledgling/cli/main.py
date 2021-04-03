# -*- coding: utf8 -*-
import click

from fledgling.cli.command.create_config import create_config
from fledgling.cli.command.create_plan import create_plan
from fledgling.cli.command.create_task import create_task
from fledgling.cli.command.event_loop import event_loop

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
    short_help=event_loop.__doc__,
)
cli.add_command(event_loop_command)


if __name__ == '__main__':
    cli()
