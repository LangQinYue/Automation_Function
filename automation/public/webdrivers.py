# -.- coding:utf-8 -.-
import sys
from selenium.webdriver.common.by import By
reload(sys)
sys.setdefaultencoding("utf-8")
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from funtion import Method
import json
from selenium import webdriver


class Web(object):
	@classmethod
	def quit_browser(cls, driver,loc_list):
		Method.save_pic(driver,loc_list)
		driver.quit()
	@classmethod
	def getby(cls,by):
		getby_dict = {'ID':By.ID,
             'CLASS_NAME':By.CLASS_NAME,
             'CSS_SELECTOR':By.CSS_SELECTOR,
             'LINK_TEXT':By.LINK_TEXT,
             'NAME':By.NAME,
             'PARTIAL_LINK_TEXT':By.PARTIAL_LINK_TEXT,
             'TAG_NAME':By.TAG_NAME,
             'XPATH':By.XPATH
             }
		try:
			if by.upper() in getby_dict:
				bytype = getby_dict[by.upper()]
			return bytype
		except Exception:
			pass

	@classmethod
	def find_element(cls, loc_list, driver):
		"""
		:param loc_list: element content list
		:param driver: selenium driver
		:return: do find element
		"""
		by = cls.getby(loc_list['method'])
		value = loc_list['content']
		for index, loc in enumerate(loc_list):
			try:
				WebDriverWait(driver, 5).until(lambda dr: driver.find_element(by,value).is_displayed())
				return driver.find_element(by,value)
			except:
				if index == 1:
					cls.quit_browser(driver,loc_list)
					raise ValueError("定位元素失败:\n元素内容:%s" % json.dumps(loc_list))
				continue

	@classmethod
	def get_text(cls, loc_list, driver):
		element_object = cls.find_element(loc_list, driver)
		try:
			return element_object.text
		except:
			return element_object.get_attribute("value")

	@classmethod
	def send_keys(cls, loc_list, input_value, driver):
		"""
		:param loc_list: element content list
		:param input_value: input value
		:param driver: selenium driver
		:return: do send keys
		"""
		element_object = cls.find_element(loc_list, driver)
		try:
			element_object.clear()
			element_object.send_keys(input_value)
		except:
			cls.quit_browser(driver)
			raise ValueError(u"输入内容失败:\n元素内容:%s" % json.dumps(loc_list))

	@classmethod
	def switch_frame(cls, loc_list, driver):
		"""
		:param loc_list: element content list
		:param driver: selenium driver
		:return: do switch frame
		"""
		element_object = cls.find_element(loc_list, driver)
		try:
			return driver.switch_to_frame(element_object)
		except:
			cls.quit_browser(driver)
			raise ValueError(u"切换frame失败:\n元素内容:%s" % json.dumps(loc_list))

	@classmethod
	def switch_to_default_content(cls, driver):
		"""
		:param driver:selenium driver
		:return: switch default content/ quit iframe
		"""
		try:
			driver.switch_to_default_content()
		except:
			cls.quit_browser(driver)
			raise ValueError(u"切换默认页面失败")

	@classmethod
	def move_to_element(cls, loc_list, driver):
		"""
		:param loc_list:element content list
		:param driver: selenium driver
		:return: move to element
		"""
		element_object = cls.find_element(loc_list, driver)
		try:
			ActionChains(driver).move_to_element(element_object).perform()
		except:
			cls.quit_browser(driver)
			raise ValueError(u"鼠标移动到元素失败:\n元素内容:%s" % json.dumps(loc_list))

	@classmethod
	def switch_next_window(cls, driver):
		"""
		:param driver:selenium driver
		:return: switch next window
		"""
		try:
			all_window_handles = driver.window_handles  # 获取所有窗口
			current_window_handles = driver.current_window_handle  # 获取当前窗口
			next_window_handls = all_window_handles[
				all_window_handles.index(current_window_handles) + 1]  # 通过当前窗口索引+1，获取到下一窗口
			driver.switch_to_window(next_window_handls)
		except:
			cls.quit_browser(driver)
			raise ValueError(u"切换到下一个窗口失败")

	@classmethod
	def switch_specified_window(cls, index, driver):
		"""
		:param index:window index (1,2,3)
		:param driver: selenium driver
		:return: switch specified window
		"""
		try:
			all_handles = self.driver.window_handles  # 获取所有窗口
			# 通过切片到指定窗口，同步编程语言与自然语言的数字开头，作-1操作
			driver.switch_to_window(all_handles[int(index) - 1])
		except:
			cls.quit_browser(driver)
			raise ValueError(u"切换到指定窗口失败")

	@classmethod
	def switch_default_window(cls, driver):
		"""
		:param driver:selenium driver
		:return: switch default window
		"""
		try:
			# 获取所有窗口,通过切片到指定窗口，同步编程语言与自然语言的数字开头，作+1操作
			driver.switch_to_window(driver.window_handles[0])
		except:
			cls.quit_browser(driver)
			raise ValueError(u"切换到默认窗口失败")

	@classmethod
	def close_window(cls, driver):
		"""
		:param driver:selenium driver
		:return: close current window
		"""
		try:
			driver.close()
		except:
			cls.quit_browser(driver)
			raise ValueError(u"关闭当前窗口失败")

	@classmethod
	def script(cls, content, driver):
		"""
		:param content:java script content
		:param driver: selenium driver
		:return: execute java script
		"""
		try:
			driver.execute_script(content)
		except:
			cls.quit_browser(driver)
			raise ValueError(u"执行JavaScript脚本失败,执行代码:", content)

	@classmethod
	def enter(cls, loc_list, driver):
		"""
		:param loc_list:element content list
		:param driver: selenium driver
		:return: enter
		"""
		element_object = cls.find_element(loc_list, driver)
		try:
			element_object.send_keys(Keys.ENTER)
		except:
			cls.quit_browser(driver)
			raise ValueError(u"模拟执行回车失败,元素内容为:%s" % json.dumps(loc_list))
