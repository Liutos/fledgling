# -*- coding: utf8 -*-
import subprocess

from fledgling.app.entity.task import Task
from fledgling.app.use_case.event_loop import IAlerter


class Alerter(IAlerter):
    def alert(self, *, plan, task: Task):
        args = []
        args.append('alerter')
        args.append('-message')
        args.append(task.brief)
        args.append('-sound')
        args.append('default')
        return subprocess.Popen(args)
