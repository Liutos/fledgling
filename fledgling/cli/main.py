# -*- coding: utf8 -*-
import click

from fledgling.cli.command.event_loop import event_loop


if __name__ == '__main__':
    cli = click.Group()
    event_loop_command = click.Command('event-loop', callback=event_loop)
    cli.add_command(event_loop_command)
    cli()
