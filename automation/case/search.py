#!/usr/bin/env python
#coding:utf-8
import unittest

from unittest.loader import defaultTestLoader
from automation.public import HTMLTestRunner
from selenium import webdriver

from case_type import Operation
from automation.public.action import ParseStep
import json
from os import path
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class TestCase(unittest.TestCase):
    @staticmethod
    def setUp(data):
        driver = webdriver.Firefox()
        print data
        


    def testMet1(self):
        u'''baidu搜索'''
        self.driver = webdriver.Firefox()
        print u'打开百度页面'
        self.driver.get('http://www.baidu.com')
        print u'搜索框输入搜索词'
        El = self.driver.find_element_by_xpath('//*[@id="kw"]')
        El.send_keys('python')
        print u'点击百度一下按钮'
        self.driver.find_element_by_id('su').click()
        self.assertTrue('百度一下',self.driver.title)
        
    def tearDown(self):
        self.driver.quit()
def suit():

#         suite = unittest.TestSuite()
#         suite.addTest(TestCase('testMet1'))
#         return suite
        #第二种
        return unittest.makeSuite(TestCase('a'), "test")#要测试的方法名都以test开头
        #传入类名和要加入套件的方法名的头部

#     testunit = unittest.TestSuite()
#     testunit.addTest(unittest.makeSuite(TestCase.testMet1))
if __name__ == '__main__':
    #第一种
    #unittest.main() #要测试的方法名都以test开头
    #第二种
    #unittest.main(defaultTest = 'suit')
    '''
            另一种执行方式：
    suite = unittest.TestSuite()
    suite.addTest(Mytest("test_add"))
    suite.addTest(Mytest("test_add2"))
    suite.addTest(Mytest("test_add3"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
    '''
#     testunit = unittest.TestSuite()
#     testunit.addTest(unittest.makeSuite(TestCase.testMet1))
#     run = unittest.TextTestRunner()
#     run.run(testunit)

    filename = 'D:\\eclipsworkdir\\lang\\testCase\\report.html'
    fp = file(filename,'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'百度搜素报告',
        description =u'用例执行情况' )
    runner.run(suit())
    fp.close()

    #unittest.main()