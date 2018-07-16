# -.- coding:utf-8 -.-
'''
使用默认的python运行先
'''
__author__ = 'lang.qy'
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(command_executor='http://172.16.34.90:5555/wd/hub',
                          desired_capabilities=DesiredCapabilities.SAFARI)
driver.get("http://www.baidu.com")
driver.find_element_by_id("kw").send_keys("hello")
driver.find_element_by_id("su").click()
time.sleep(2)
driver.quit()
driver.maximize_window()
