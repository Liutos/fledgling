# -*- coding: utf8 -*-
import datetime

from fledgling.app.use_case.event_loop import IDoNotDisturbService


class DoNotDisturbService(IDoNotDisturbService):
    def check_do_not_disturb(self, begin_time: datetime.time, end_time: datetime.time,
                             *, now: datetime.datetime = None) -> bool:
        if now is None:
            now = datetime.datetime.now()

        begin_datetime = now.replace(hour=begin_time.hour, minute=begin_time.minute, second=0)
        end_datetime = now.replace(hour=end_time.hour, minute=end_time.minute, second=0)
        if end_time < begin_time:
            end_datetime += datetime.timedelta(days=1)

        return begin_datetime < now <= end_datetime
