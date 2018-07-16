# -.- coding:utf-8 -.-
__author__ = 'lang.qy'
import sys

#sys.path.append("..")
import json
from automation.public.db import DB


class Operation(object):
	def __init__(self):
		pass
	def choose(self,data):
		if hasattr(self, data.get("type", None)):
			return getattr(self, data["type"])(data)
		else:
			raise AttributeError("未知的用例类型")

	def case(self,data):
		#data={'ip': '127.0.0.1', 'type': 'case', 'id': 12}
		case_content = DB.case(data["id"])
		case_content["ip"] = data["ip"]
		case_content["type"] = data["type"]
		case_list=[]
		case_list.append(case_content)
		return case_list

	def suite(self, data):
		"""
		:param data:suite dict data
		:return: case list
		"""
		return DB.suite_parse_case(data)


if __name__ == "__main__":
 	operation = Operation()
 	data = {'ip': '127.0.0.1', 'type': 'case', 'id': 12}
 	#getattr(operation,data["type"],'default')(data)
 	print operation.choose(data)


'''
class A:   
    def __init__(self):   
        self.name = 'zhangjing'  

    def method(self,name):   
        print"method print"  
        print name
  
Instance = A()   
print getattr(Instance ,'name','not find')#如果Instance 对象中有属性name则打印self.name的值，否则打印'not find'
print getattr(Instance ,'age','not find')  #如果Instance 对象中有属性age则打印self.age的值，否则打印'not find'
print getattr(Instance,'method','default')   
#如果有方法method，否则打印其地址，否则打印default  
print getattr(Instance,'method','default')('aaa')   
#如果有方法method，运行函数并打印None否则打印default  
'''