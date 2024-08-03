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

        time_ranges = []
        if begin_time < end_time:
            begin_datetime = now.replace(hour=begin_time.hour, minute=begin_time.minute, second=0)
            end_datetime = now.replace(hour=end_time.hour, minute=end_time.minute, second=0)
            time_ranges.append([begin_datetime, end_datetime])
        elif begin_time == end_time:
            pass
        else:
            # 如果开始的时间比结束的时间大，说明勿扰时段实际上由两部分组成：
            # 1. 今天的零点到今天的 end_time。以及；
            # 2. 今天到 begin_time 到明天的零点；
            today_zero = now.replace(hour=0, minute=0, second=0)
            end_datetime = today_zero.replace(hour=end_time.hour, minute=end_time.minute)
            time_ranges.append([today_zero, end_datetime])
            begin_datetime = now.replace(hour=begin_time.hour, minute=begin_time.minute, second=0)
            tomorrow_zero = now.replace(hour=0, minute=0, second=0) + datetime.timedelta(days=1)
            time_ranges.append([begin_datetime, tomorrow_zero])

        reasons = []
        for begin_datetime, end_datetime in time_ranges:
            do_not_disturb = begin_datetime < now <= end_datetime
            _format = '%Y-%m-%d %H:%M:%S'
            reason = '当前时间 %s %s起点 %s 和终点 %s之间，%s拉取计划' % (
                now.strftime(_format),
                '在' if do_not_disturb else '不在',
                begin_datetime.strftime(_format),
                end_datetime.strftime(_format),
                '不需要' if do_not_disturb else '需要',
            )
            if do_not_disturb:
                return do_not_disturb, reason

            reasons.append(reason)

        return False, '，并且'.join(reasons)
