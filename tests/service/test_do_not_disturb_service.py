import datetime
import unittest

from fledgling.service.do_not_disturb import DoNotDisturbService


class DoNotDisturbServiceTestCase(unittest.TestCase):
    def test_check_do_not_disturb_no(self):
        """测试当前时间落在了勿扰时间段之外的场景。"""
        service = DoNotDisturbService()
        self.assertFalse(service.check_do_not_disturb(
            datetime.time(hour=15, minute=00),
            datetime.time(hour=16, minute=31),
            now=datetime.datetime(2023, 3, 26, 17, 32)
        ))

    def test_check_do_not_disturb_yes(self):
        """测试当前时间落在了勿扰时间段之内的场景。"""
        service = DoNotDisturbService()
        self.assertTrue(service.check_do_not_disturb(
            datetime.time(hour=15, minute=00),
            datetime.time(hour=16, minute=31),
            now=datetime.datetime(2023, 3, 26, 15, 32)
        ))

    def test_check_do_not_disturb_yes2(self):
        """测试当前时间落在了勿扰时间段之内、并且结束时间在第二天的场景。"""
        service = DoNotDisturbService()
        self.assertTrue(service.check_do_not_disturb(
            datetime.time(hour=15, minute=00),
            datetime.time(hour=1, minute=31),
            now=datetime.datetime(2023, 3, 26, 17, 32)
        ))

    def test_check_do_not_disturb_yes3(self):
        """测试当前时间已经是第二天、并且早于结束时间的场景。"""
        service = DoNotDisturbService()
        do_not_disturb, reason = service.check_do_not_disturb_with_reason(
            datetime.time(hour=23, minute=00),
            datetime.time(hour=9, minute=0),
            now=datetime.datetime(2024, 8, 2, 2, 31)
        )
        print('reason', reason)
        self.assertTrue(do_not_disturb)


if __name__ == '__main__':
    unittest.main()
