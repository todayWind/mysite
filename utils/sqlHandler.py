import pymysql
import logging
from utils.logHandler import LogHandler


class MySqlDb(object):
    Log = LogHandler().log_fun()

    def __init__(self):
        # 建立连接

        self.conn = pymysql.connect(host='124.220.179.221', port=3307, user='root', password='123456',
                                    database='iruance_cms')
        # 创建游标
        self.cur = self.conn.cursor()
        # self.cur = self.conn.cursor(pymysql.cursors.DictCursor)  # 返回字典型的数据

    def operate_sql(self, data_dict, sql):
        """
        处理sql
        :param data_dict:
        :param sql:
        :return:
        """
        if sql.lower().startswith('select'):
            select_sql = self.select_data(sql,data_dict)
            return select_sql
        elif sql.lower().startswith('delete'):
            del_sql = self.del_data(sql,data_dict)
            return del_sql
        elif sql.startswith('update'):
            update_sql = self.update_data(sql,data_dict)
            return update_sql
        elif sql.lower().startswith('insert'):
            insert_sql = self.insert_data(sql,data_dict)
            return insert_sql
        else:
            logging.info(f'{data_dict.get("case_id")}用例,{data_dict.get("desc")}接口,sql语句错误')

    def check_sql(self, data_dict, sql):
        """
        检查sql
        :param data_dict:
        :param sql:
        :return:
        """
        if ';' in sql:
            sql = sql.split(';')

        if isinstance(sql, list):
            result_lst = []
            for i in sql:
                result_lst.append(self.operate_sql(data_dict, i))
            return result_lst
        else:
            return self.operate_sql(data_dict, sql)

    def select_data(self, select_sql,data_dict):
        """查看操作"""
        try:
            self.cur.execute(select_sql)
            data = self.cur.fetchall()
            return data

        except Exception as e:
            logging.error(f'{data_dict.get("case_id")}用例,{data_dict.get("desc")},sql语句"数据查询失败": {str(e)}')

            return "sql语句数据查询失败" + str(e)

    def insert_data(self, insert_sql,data_dict):

        try:
            self.cur.execute(insert_sql)
            self.conn.commit()  # 这里一定要commit才行，要不然数据是不会插入的
            logging.info(f'{data_dict.get("case_id")}用例,{data_dict.get("desc")},sql语句"插入数据成功"')

            return "插入数据成功"
        except Exception as e:
            self.conn.rollback()  # 发生错误时回滚
            logging.error(f'{data_dict.get("case_id")}用例,{data_dict.get("desc")},sql语句"插入数据失败": {str(e)}')

            return "sql语句插入语句执行错误" + str(e)

    def del_data(self, del_sql,data_dict):
        # 删除操作
        try:
            self.cur.execute(del_sql)
            self.conn.commit()
            logging.info(f'{data_dict.get("case_id")}用例,{data_dict.get("desc")},sql语句"删除数据成功"')
            return "sql语句数据删除成功"
        except Exception as e:
            self.conn.rollback()  # 发生错误时回滚
            logging.error(f'{data_dict.get("case_id")}用例,{data_dict.get("desc")},sql语句"删除数据失败": {str(e)}')

            return "sql语句删除语句执行错误" + str(e)

    def update_data(self, update_sql,data_dict):
        # 修改操作
        try:
            self.cur.execute(update_sql)
            self.conn.commit()
            logging.info(f'{data_dict.get("case_id")}用例,{data_dict.get("desc")},sql语句"修改数据成功"')

            return "sql语句数据更新成功"
        except Exception as e:
            self.conn.rollback()  # 发生错误时回滚
            logging.error(f'{data_dict.get("case_id")}用例,{data_dict.get("desc")},sql语句"修改数据失败": {str(e)}')

            return "sql语句修改语句执行错误" + str(e)


if __name__ == '__main__':
    mySql = MySqlDb()
