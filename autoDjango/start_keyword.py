# -.- coding:utf-8 -.-
__author__ = 'lang.qy'
from os import path
import json
import os
from automation.case.run_case import run

def start_case(case_id, current_ip, _type):
	"""
	:param case_id: case id
	:param current_ip: current ip
	:param _type: type
	:return:
	"""
	try:
		case_path = path.dirname(path.dirname(path.abspath(__file__))) + "/automation/case/config.json"
		try:
			with open(case_path, 'w') as f:
				f.write(json.dumps({"id": case_id, "ip": current_ip, "type": _type}))
		except:
			raise ValueError(u"写入用例信息失败")
		'''
		automation_path = path.dirname(path.dirname(path.abspath(__file__))) + "/automation/case/run_case.py"
		python_path = "python" + " "
		os.system(python_path + automation_path)
		return True
		'''
		run()
	except:
		return False
#start_case(15,"127.0.0.1","case")