# -*- coding: utf8 -*-
"""存放在不止一处用到的枚举值的定义。"""
from enum import Enum

from fledgling.app.entity import task


class RepeatTypeEnum(Enum):
    DAILY = ('daily', '表示每过24小时重复一次')
    END_OF_MONTH = ('end_of_month', '表示在每个月的最后一天重复一次')
    HOURLY = ('hourly', '表示每小时重复一次')
    MONTHLY = ('monthly', '表示每个月的同一天重复一次')
    PERIODICALLY = ('periodically', '表示每过一段由`--repeat-interval`指定的时间重复一次')
    WEEKLY = ('weekly', '表示每7天重复一次')


class StatusEnum(Enum):
    """表示任务状态的枚举类。"""
    CREATED = (task.TaskStatus.CREATED.value, '新建')
    FINISHED = (task.TaskStatus.FINISHED.value, '已完成')
    CANCELLED = (task.TaskStatus.CANCELLED.value, '已取消')


# 参见[这里](https://click.palletsprojects.com/en/8.0.x/documentation/#preventing-rewrapping)
# 的方法，用单独一行 \b 提示 click 保留帮助消息中的换行符。
REPEAT_TYPE_HELP = '\b\n' + '\n'.join(['- ' + e.value[0] + ' ' + e.value[1] for e in RepeatTypeEnum])
STATUS_HELP = '\b\n' + '\n'.join(['- ' + str(e.value[0]) + ' ' + e.value[1] for e in StatusEnum])

REPEAT_TYPES = list([e.value[0] for e in RepeatTypeEnum])
STATUS = list([str(e.value[0]) for e in StatusEnum])
