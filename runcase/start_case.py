import unittest
import os
from HTMLTestRunner import HTMLTestRunner
from conf import settings
from utils.emailHandler import EmailHandler


class RunDiscover(unittest.TestCase):
    em = EmailHandler()
    START_DIR = settings.TESTCASE_DIR
    TOP_LEVEL_DIR = settings.TESTCASE_DIR
    REPORT_DIR = settings.REPORT_PATH
    f = open(REPORT_DIR, 'wb')

    def run_all_testcase(self):
        suite = unittest.TestLoader().discover(
            start_dir=self.START_DIR,
            pattern='test*.py',
        )
        HTMLTestRunner(
            stream=self.f,
            verbosity=2,
            title='自动化测试报告',
            description=''
        ).run(suite)

    def run_send_email(self, status: bool = False):
        print('status',status)
        return self.em.send_email(status)


if __name__ == '__main__':
    run_case = RunDiscover()
    run_case.run_all_testcase()
    run_case.run_send_email(True)
