# -.- coding:utf-8 -.-
__author__ = 'lang.qy'

from os import path
import os

os.chdir(path.dirname(path.abspath(__file__)))


import unittest
import time
import json
import startcase
import sys
sys.path.append("..")
from automation.public import HTMLTestRunner


class KeyWordTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self, map(search.TestCase,
                                              ("testMet1" )))

class Start(object):
	@classmethod
	def test_suite(cls):
		
 		suite = unittest.TestSuite()
 		suite.addTest(unittest.makeSuite(startcase.KeyWord))
		return suite
		
        #return start_case.run()

	@classmethod
	def filename_django(cls):
		with open("config.json") as f:
			case_config = json.loads(f.read())
		filename = path.dirname(path.abspath('..')) + "/templates/report/{}-{}.html".format(
				case_config['type'],
				case_config['id'])
		return filename

	@classmethod
	def filename(cls):
		now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		tdresult = '../result/' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
		if os.path.exists(tdresult):
			filename = tdresult + "/" + now + "_result.html"
		else:
			os.makedirs(tdresult)
			filename = tdresult + "/" + now + "_result.html"
		return filename

	@classmethod
	def run(cls):
		fp = file(cls.filename_django(), "wb")
		runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"自动化测试报告", description=u"用例执行情况:")
		runner.run(cls.test_suite())
		fp.close()


def run():
	Start.run()
	
