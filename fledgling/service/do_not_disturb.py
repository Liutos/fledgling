# -*- coding: utf8 -*-
import datetime
import typing

from fledgling.app.use_case.event_loop import IDoNotDisturbService


class DoNotDisturbService(IDoNotDisturbService):
    def check_do_not_disturb(self, begin_time: datetime.time, end_time: datetime.time,
                             *, now: datetime.datetime = None) -> bool:
        return self.check_do_not_disturb_with_reason(begin_time, end_time, now=now)[0]

    def check_do_not_disturb_with_reason(self, begin_time: datetime.time, end_time: datetime.time,
                                         *, now: datetime.datetime = None) -> typing.Tuple[bool, str]:
        if now is None:
            now = datetime.datetime.now()

        begin_datetime = now.replace(hour=begin_time.hour, minute=begin_time.minute, second=0)
        end_datetime = now.replace(hour=end_time.hour, minute=end_time.minute, second=0)
        is_tomorrow = False
        if end_time < begin_time:
            end_datetime += datetime.timedelta(days=1)
            is_tomorrow = True

        do_not_disturb = begin_datetime < now <= end_datetime
        _format = '%Y-%m-%d %H:%M:%S'
        reason = '当前时间 %s %s起点 %s 和终点 %s%s之间，%s拉取计划' % (
            now.strftime(_format),
            '在' if do_not_disturb else '不在',
            begin_datetime.strftime(_format),
            end_datetime.strftime(_format),
            '（明天）' if is_tomorrow else '',
            '不需要' if do_not_disturb else '需要',
        )
        return do_not_disturb, reason
