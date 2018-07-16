# -.- coding:utf-8 -.-
__author__ = 'lang.qy'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import webdrivers
from db import DB
from webdrivers import Web
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep


class ParseStep(object):
	def __init__(self, data):
		self.data = data

	def run_step(self):
		action = Action()
		driver = action.driver(None)
		# driver = action.driver(self.data["ip"])
		action.start_browser(self.data, driver)
		error_list = []
		for index, step in enumerate(DB.step(self.data["id"])):
			print(str(index + 1) + ":" + step['desc'] + " " + step["value"])
			_assert = action.get_action(step, driver)
			if _assert:
				error_list.extend(_assert)
			sleep(1)
		driver.quit()
		return error_list


class Action(object):
	def driver(self, ip=None):
		"""
		:param ip:remote ip
		:return: driver
		"""
		if ip is None:
			return webdriver.Firefox()
		else:
			client_ip = 'http://{ip}:5555/wd/hub'.format(ip=ip)
			remote_driver = webdriver.Remote(command_executor=client_ip,
			                                 desired_capabilities=DesiredCapabilities.FIREFOX)
			return remote_driver

	def get_action(self, data, driver):
		if hasattr(self, data.get("keyword", None)):
			getattr(self, data["keyword"])(data, driver)
		else:
			raise AttributeError("没有该关键字方法")
	
	def quit(self,driver,loc_list):
		Web.quit_browser(driver, loc_list)

	def set_size(self, driver):
		"""
		:param driver:web driver
		:return: set window size
		"""
		try:
			# driver.set_window_size("414", "736")  # iphone6 plus
			driver.maximize_window()
		except:
			raise ValueError("Set Size Error")

	def loc(self, step):
		"""
		:param step:step data
		:return: element content list
		"""
		return DB.element(step['element'])[0]

	def start_browser(self, data, driver):
		"""
		:param data: case data
		:param driver: selenium driver
		:return: open url
		"""
		self.set_size(driver)
		url = DB.url(data["id"])

		driver.get(url)
		print "\n用例名称:{} \n用例类型:{} 用例状态:{} 用例等级:{}".format(data["name"], data["nature"], data["status"], data["level"])
		print "\n测试过程:"

	def click(self, step, driver):
		"""
		:param step: case step data
		:param driver: selenium driver
		:return: click button
		"""
		Web.find_element(self.loc(step), driver).click()

	def input(self, step, driver):
		"""
		:param step:case step data
		:param driver: selenium driver
		:return: input values
		"""
		value = step.get("value", "").strip()
		if value:
			Web.send_keys(self.loc(step), step['value'], driver)

	def quit(self, driver):
		"""
		:param driver:selenium driver
		:return: browser quit
		"""
		Web.quit_browser(driver)

	def import_case(self, driver):
		"""
		导入用例关键字,可以忽略
		:param driver: selenium driver
		:return:
		"""
		pass

	def get_url(self, step, driver):
		"""
		:param step:step data
		:param driver: selenium driver
		:return:
		"""
		value = step.get("value", "").strip()
		driver.get(value)

	def assert_text(self, step, driver):
		"""
		取值断言,失败则返回预期值交给unittest处理
		:param step: step data
		:param driver: selenium driver
		:return: assert error values
		"""
		get_text = Web.get_text(self.loc(step), driver)
		print("""\n开始取值断言:\n预期值:%s\n取值:%s""" % (step['value'], get_text))
		if step['value'] != get_text:
			print("断言结果:测试不通过")
			return step['value']
		else:
			print("断言结果:测试通过")
