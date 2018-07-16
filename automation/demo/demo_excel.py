# coding=utf-8
__author__ = 'radiateboy'

import unittest
import xlrd

class  MyTestCase(unittest.TestCase):

	def test_xls(self):

		# 获取一个工作表、行和列的值（数组），行数和列数
		# .encode('gb18030')
		# .encode('utf-8')
		# .encode('cp936')
		# .decode('utf-8').encode(types)

		data = xlrd.open_workbook(u"..\\data\\login_126mail_data.xls")
		#通过索引顺序获取
		table = data.sheets()[0]
		#通过索引顺序获取
		table1 = data.sheet_by_index(0)
		#通过名称获取
		table2 = data.sheet_by_name(u'Sheet1')

		i = 1
		#获取整行和整列的值（数组）
		print table1.row_values(0)
		print table.col_values(i)
		print table1.col_values(i)
		print table2.col_values(i)


		#获取行数和列数
		nrows = table.nrows
		print nrows
		ncols = table.ncols
		print  ncols

		#循环行列表数据
		for i in range(1, nrows):
			txt =  table.row_values(i)
			print txt

		#读取单元格
		print "读取单元格"
		cell_A1 = table.cell(0, 0).value
		print "A1: " + cell_A1
		cell_C3 = table.cell(2, 2).value
		print "C3: " + cell_C3

		#使用行列索引
		cell_A1 = table.row(0)[0].value
		print cell_A1
		cell_A2 = table.col(1)[0].value
		print cell_A2

if __name__ == '__main__':
	unittest.main()
