# -*- coding: utf8 -*-
import subprocess
from typing import List

from fledgling.app.entity.task import Task
from fledgling.app.use_case.event_loop import IAlerter


class Alerter(IAlerter):
    def alert(self, *, plan, task: Task):
        args: List[str] = []
        args.append('alerter')
        args.append('-title')
        args.append('#{} {}'.format(task.id, task.brief))
        args.append('-sound')
        args.append('default')
        if isinstance(plan.duration, int) and plan.duration > 0:
            args.extend(['-timeout', str(plan.duration)])
            args.extend(['-message', '展示{}秒后自动关闭'.format(plan.duration)])
        else:
            args.extend(['-message', '需要手动关闭'])
        args.extend(['-group', str(task.id)])
        return subprocess.Popen(args)
