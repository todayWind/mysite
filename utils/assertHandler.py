import unittest
import logging
import json
from utils.sqlHandler import MySqlDb
from bs4 import BeautifulSoup


class AssertHandler(unittest.TestCase):
    mySql = MySqlDb()

    def assert_func(self, data_dict, response, case_id, desc, teardown_sql=None, expect_result=None, except_sql=None):
        if expect_result:
            if 'application/json' in response.headers['Content-Type'].lower():
                # 第一层返回值校验
                self.assertIn(expect_result, json.dumps(response.json(), ensure_ascii=False))
                if teardown_sql:
                    # 第二层数据库校验
                    ret_sql = self.mySql.check_sql(data_dict, teardown_sql)
                    if ret_sql:
                        if except_sql:
                            self.assertEqual(except_sql, ret_sql[0][0])
                            logging.info(f'{case_id}用例,{desc},测试通过!')
                            return '测试通过!'
                        else:
                            logging.warning(f'{case_id}用例,{desc},预期数据库结果为空!')
                    else:
                        logging.warning(f'{case_id}用例,{desc},数据库查询的返回结果为空!')
                else:
                    logging.warning(f'{case_id}用例,{desc},第一层校验测试通过!')
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                self.assertEqual(expect_result, soup.find(name='title'))
                return soup.find(name='title')
        elif teardown_sql and except_sql:
            # 第二层数据库校验
            ret_sql = self.mySql.check_sql(data_dict, teardown_sql)
            self.assertEqual(except_sql, ret_sql[0][0])
            logging.info(f'{case_id}用例,{desc},数据库校验通过,测试通过!')
            return '数据库校验通过'

        elif teardown_sql:
            ret_sql = self.mySql.check_sql(data_dict, teardown_sql)
            logging.warning(f'{case_id}用例,{desc},该用例只进行了后置处理!!')
            return ret_sql
        else:
            logging.warning(f'{case_id}用例,{desc},没有断言没有数据库校验没有后置处理!!!')


if __name__ == '__main__':
    AssertHandler()
