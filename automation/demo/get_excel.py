# -.- coding:utf-8 -.-
__author__ = 'Administrator'
import sys
import xlrd
reload(sys)
sys.setdefaultencoding("utf-8")
def xls_key(val):
    """取元素"""
    data = xlrd.open_workbook('..\\data\\data.xls')
    table = data.sheet_by_name(u"页面元素表")
    nrows = table.nrows
    for i in range(0, nrows):
        if val == table.row_values(i)[0]:
            return tuple(table.row_values(i)[1:3])

def get_case(val):
    """取元素"""
    data = xlrd.open_workbook('..\\data\\data.xls')
    table = data.sheet_by_name(u"测试用例表")
    nrows = table.nrows
    for i in range(0, nrows):
        if val == table.row_values(i)[0]:
            return table.row_values(i)

def get_base(val):
    """取元素"""
    data = xlrd.open_workbook('..\\data\\data.xls')
    table = data.sheet_by_name(u"基本设置表")
    nrows = table.nrows
    for i in range(0, nrows):
        if val == table.row_values(i)[0]:
            return table.row_values(i)

def get_assert(val):
    """取元素"""
    data = xlrd.open_workbook('..\\data\\data.xls')
    table = data.sheet_by_name(u"取值元素表")
    nrows = table.nrows
    for i in range(0, nrows):
        if val == table.row_values(i)[0]:
            return tuple(table.row_values(i)[1:3])