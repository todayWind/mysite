import requests
import json
import logging
import re
from utils.readExcel import ReadExcel
from utils.logHandler import LogHandler
from utils.sqlHandler import MySqlDb
from conf import settings
from jsonpath_rw import parse


class SendRequests:

    def __init__(self, data_list=None):
        self.Log = LogHandler().log_fun()
        self.mySql = MySqlDb()
        self.data_list = data_list

    def send_request(self, data_dict, cookies={}):

        url = data_dict.get('url')  # 接口的url地址

        # 发送请求
        response = requests.request(
            method=self.check_method(data_dict),
            url=url,
            params=self.check_request_params(data_dict),
            data=self.check_request_data(data_dict),
            json=self.check_request_json(data_dict),
            headers=self.check_request_headers(data_dict),
            cookies=cookies)
        self.save_info(response, data_dict)
        return response

    def check_method(self, data_dict):
        _METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
        method = data_dict.get('method')
        if method:
            if method.upper() in _METHODS:
                return method
            else:
                logging.error(f'{data_dict.get("case_id")}用例,method错误!!!')
                return
        else:
            logging.error(f'{data_dict.get("case_id")}用例,method为空!!!')
            return

    def check_request_params(self, data_dict):
        # 这个是属于get请求中的url中参数的提交方式
        params = data_dict.get('params')
        if params:

            check_params = self.operate_re_sql(params, data_dict)
            return self.operate_re_msg(check_params)
        else:
            return {}

    def check_request_data(self, data_dict):
        data = data_dict.get("data")
        if data:
            check_data = self.operate_re_sql(data, data_dict)
            return self.operate_re_msg(check_data)
        else:
            return {}

    def check_request_json(self, data_dict):
        json_data = data_dict.get("json")
        if json_data:
            check_json = self.operate_re_sql(json_data, data_dict)
            return self.operate_re_msg(check_json)
        else:
            return {}

    def check_request_headers(self, data_dict):
        headers = data_dict.get("headers")
        if headers:
            check_headers = self.operate_re_sql(headers, data_dict)
            return self.operate_re_msg(check_headers)
        else:
            return {}

    def operate_re_sql(self, parameter, data_dict):
        """
        处理依赖数据库动态数据
        :param parameter:
        :param data_dict:
        :return:
        """
        if isinstance(parameter, dict):
            parameter = json.dumps(parameter)
        pattern = re.compile('sql{(.*?)}sql')  # 正则规则
        rule_list = pattern.findall(parameter)
        if rule_list:
            print('rule_list', rule_list)
            for rule in rule_list:
                {"ids": "sql{select id from sys_user where user_name='wind2333'>ids}sql"}
                cat_sql, json_path = rule.split('>')
                select_data = self.mySql.select_data(cat_sql, data_dict)
                if select_data:
                    parameter = re.sub(pattern=pattern, repl=str(select_data[0][0]), string=parameter, count=1)
                    print('parameter---', parameter)
            return json.loads(parameter)
        else:
            if isinstance(parameter, str):
                parameter = json.loads(parameter)
                return parameter

    def operate_re_msg(self, parameter):
        """正则校验数据依赖的字段"""
        if isinstance(parameter, dict):
            parameter = json.dumps(parameter)
        pattern = re.compile(r'\${(.*?)}\$')  # 正则规则
        rule_list = pattern.findall(parameter.strip())
        print('rule_list', rule_list)
        if rule_list:  # 该参数有数据依赖
            for rule in rule_list:
                {"access_token": "${case_1>response_json>access_token}$"}
                case_id, params, json_path = rule.split('>')
                for line in self.data_list:
                    if str(line['case_id']) == case_id:
                        temp_data = line['temporary_{}'.format(params)]
                        if isinstance(temp_data, str):
                            temp_data = json.loads(temp_data)
                        match_list = parse(json_path).find(temp_data)
                        if match_list:
                            match_data = [v.value for v in match_list][0]
                            # 将提取出来的值替换到原来规则
                            parameter = re.sub(pattern=pattern, repl=str(match_data), string=parameter, count=1)
                            print('parameter----', parameter)
            return json.loads(parameter)
        else:
            if isinstance(parameter, str):
                parameter = json.loads(parameter)
                return parameter

    def save_info(self, response, data_dict):
        """
        存储信息
        :param response:
        :return:
        """
        for item in self.data_list:
            if item.get('case_id') == data_dict.get('case_id'):
                item['temporary_response_cookies'] = response.cookies.get_dict()
                item['temporary_request_headers'] = data_dict.get('headers')
                item['temporary_request_data'] = data_dict.get('data')
                item['temporary_request_json'] = data_dict.get('json')
                item['temporary_request_params'] = data_dict.get('params')
                item['temporary_response_headers'] = response.headers
                if 'application/json' in response.headers['Content-Type'].lower():
                    item['temporary_response_json'] = response.json()
                else:
                    item['temporary_response_text'] = response.text

        return response


if __name__ == '__main__':
    t = ReadExcel(settings.EXCEL_PATH, settings.EXCEL_SHEET_NAME)
    t.read_excel()
