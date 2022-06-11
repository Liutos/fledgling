# -*- coding: utf8 -*-
from typing import List
import subprocess
import logging

import requests

from fledgling.app.entity.plan import Plan
from fledgling.app.entity.task import Task
from fledgling.app.use_case.event_loop import IAlerter


class Alerter(IAlerter):
    def alert(self, *, plan: Plan, task: Task):
        args: List[str] = []
        args.append('alerter')
        args.append('-title')
        args.append('#{} {}'.format(task.id, task.brief))
        args.append('-sound')
        args.append('default')
        args.append('-subtitle')
        args.append('预定于' + plan.trigger_time.strftime('%Y-%m-%d %H:%M:%S') + '触发')
        if isinstance(plan.duration, int) and plan.duration > 0:
            args.extend(['-timeout', str(plan.duration)])
            args.extend(['-message', '展示{}秒后自动关闭'.format(plan.duration)])
        else:
            args.extend(['-message', '需要手动关闭'])
        args.extend(['-group', str(task.id)])
        return subprocess.Popen(args)


class FacadeAlerter(IAlerter):
    """负责发送多种形式的消息的通知类。"""
    def __init__(self, alerter: IAlerter, wechat_alerter: IAlerter):
        self.alerter = alerter
        self.wechat_alerter = wechat_alerter

    def alert(self, *, plan: Plan, task: Task):
        """发送微信消息和桌面通知。"""
        self.wechat_alerter.alert(plan=plan, task=task)
        return self.alerter.alert(plan=plan, task=task)


class WeChatAlerter(IAlerter):
    """负责发送微信消息的通知类。"""
    def __init__(self, send_key: str):
        self.send_key = send_key

    def alert(self, *, plan: Plan, task: Task):
        # server 酱的接口文档：https://sct.ftqq.com/sendkey
        url = 'https://sctapi.ftqq.com/{}.send'.format(self.send_key)
        data = {
            'desp': task.brief,
            'title': task.brief[:32],  # server 酱的 title 的最大长度为 32。
        }
        response = requests.post(url, data=data)
        logging.debug('发送了微信消息：{}'.format(response.text))
        return None
