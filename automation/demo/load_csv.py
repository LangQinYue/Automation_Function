# -*- coding: utf-8 -*-
import csv, sys, os, xlrd, time
from selenium import webdriver

reload(sys)
reload(sys)
sys.setdefaultencoding("utf-8")


class Data():
    @staticmethod
    # 使用静态方法打开CSV返回一个列表
    def csv_data():
        my_csv = "D:\\python\\Python-Selenium\\PageObject\\data\\data.csv"
        csv_iteration = csv.reader(file(my_csv, "rb"))
        for csv_list in csv_iteration:
            return csv_list

    @staticmethod
    def xls_data(sheet="login", keyword='baidu'):
        data = xlrd.open_workbook("D:\\python\\Python-Selenium\\PageObject\\data\\data.xls")
        table = data.sheet_by_name(sheet)
        nrows = table.nrows
        for i in range(0, nrows):
            if keyword in table.row_values(i):
                return table.row_values(i)

# 静态方法无需实例化，可以直接调用
print Data.csv_data()
print Data.xls_data()

#下面是例子，需运行去掉注释！
# driver=webdriver.Chrome()
# driver.get("http://www.baidu.com")
# baidu_data=Data.xls_data('login','baidu')
# for i in baidu_data:
#     driver.find_element_by_id("kw").send_keys(i)
#     driver.find_element_by_css_selector("a.toindex").click()
#     time.sleep(1)

