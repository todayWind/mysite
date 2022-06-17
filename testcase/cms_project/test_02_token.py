import unittest
import logging
import os
from ddt import ddt, data, unpack
from utils.sendRequests import SendRequests
from utils.readExcel import ReadExcel
from utils.logHandler import LogHandler
from utils.sqlHandler import MySqlDb
from utils.assertHandler import AssertHandler
from conf import settings


@ddt
class Test2(unittest.TestCase):
    EXCEL_PATH = os.path.join(settings.EXCEL_DIR, 'test1.xls')
    data_list = ReadExcel(EXCEL_PATH, settings.EXCEL_SHEET_NAME).read_excel()
    print(data_list)
    Log = LogHandler().log_fun()
    mySql = MySqlDb()
    Assert = AssertHandler()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @data(*data_list)
    def test_cms(self, data_dict):
        case_id = data_dict.get('case_id')
        desc = data_dict.get('desc')
        url = data_dict.get('url')
        setup_sql = data_dict.get('setup_sql')
        teardown_sql = data_dict.get('teardown_sql')
        expect_result = data_dict.get('预期结果')
        except_sql = data_dict.get('预期数据库返回的结果')
        if setup_sql:
            self.mySql.check_sql(data_dict, setup_sql)
        logging.info('正在向 {} 发送请求，{},{}'.format(url, case_id, desc))
        response = SendRequests(self.data_list).send_request(data_dict)  # 调用公共模块执行用例

        ret_assert = self.Assert.assert_func(data_dict, response, case_id, desc, teardown_sql, expect_result,
                                             except_sql)
        return ret_assert


if __name__ == '__main__':
    Test2()
