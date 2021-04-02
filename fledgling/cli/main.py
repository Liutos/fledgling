# -*- coding: utf8 -*-
import click

from fledgling.cli.command.create_plan import create_plan
from fledgling.cli.command.create_task import create_task
from fledgling.cli.command.event_loop import event_loop

cli = click.Group()

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
    ]
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
    ]
)
cli.add_command(create_task_command)

event_loop_command = click.Command('event-loop', callback=event_loop)
cli.add_command(event_loop_command)


if __name__ == '__main__':
    cli()
