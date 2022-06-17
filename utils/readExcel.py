import xlrd
from xlutils import copy
from conf import settings


class ReadExcel:
    def __init__(self, excel_path, sheet_name):
        self.excel_path = excel_path
        self.sheet_name = sheet_name
        self.work_book = xlrd.open_workbook(self.excel_path, formatting_info=True)
        self.work_sheet = self.work_book.sheet_by_name(self.sheet_name)
        # 拷贝
        self.new_work_book = copy.copy(self.work_book)
        # 取拷贝的excel的sheet  --sheet下标(默认从0开始)
        self.new_sheet = self.new_work_book.get_sheet(0)
        # 获取总行数、总列数
        self.nrows = self.work_sheet.nrows  # 获取总行数
        self.ncols = self.work_sheet.ncols  # 获取总列数

    def read_excel(self):

        # 先判断表格中是否有内容
        if self.nrows > 1:
            # 获取第一列的内容，列表格式:0代表第一行，依次类推
            keys = self.work_sheet.row_values(0)
            # print('keys1111111',keys)

            data_list = []
            # 获取每一行的内容，列表格式
            for row in range(1, self.nrows):  # 根据索引从第二行开始取，直到去完所有的行
                values = self.work_sheet.row_values(row)
                api_dict = dict(zip(keys, values))
                data_list.append(api_dict)  # 添加到列表中去
            # print(data_list)
            return data_list
        else:
            print("表格未填写数据")
            return None


if __name__ == '__main__':
    t = ReadExcel(settings.EXCEL_PATH, settings.EXCEL_SHEET_NAME)  # 实例化
    t.read_excel()
