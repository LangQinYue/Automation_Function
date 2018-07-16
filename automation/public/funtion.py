# -.- coding:utf-8 -.-
__author__ = 'lang.qy'
import sys
import time
import os
import smtplib
from email.mime.text import MIMEText
# import MySQLdb
# import MySQLdb.cursors
from os import path

reload(sys)
sys.setdefaultencoding("utf-8")
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from time import sleep


class Method(object):
	@staticmethod
	def save_pic(driver,loc_list):
		"""
		:param driver:selenium driver
		:return:
		"""
		try:
			sleep(2)
			tm = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
			day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
			fp = os.path.dirname(os.getcwd()) + "\\result\\" + day + "\\image"
			if os.path.exists(fp):
				pic_path = str(fp) + "\\" + loc_list['name'] + ".png"
			else:
				os.makedirs(fp)
				pic_path = str(fp) + "\\" + loc_list['name'] + ".png"
			#driver.get_screenshot_as_file(pic_path)
			driver.save_screenshot(pic_path)
			
			print u'截图保存路径为:\n%s' % os.path.abspath(pic_path)
			try:
				import shutil
				django_report_image = path.dirname(
						path.abspath(path.dirname(path.dirname(__file__)))) + "/templates/report/image/"
				shutil.copy(pic_path, django_report_image)
			except:
				print "复制截图到平台失败"
		except:
			print u'保存成功截图失败'

	def send_mail(self, report_url):
		"""
		HTML方式foxmail和网页都可以正常显示文字
		说明见文字邮件版本
		:param report_url:
		:return:
		"""
		sender = "zhuzhuainiyo1@163.com"
		receiver = "48470673@qq.com"
		smtpserver = "stmp.163.com"
		username, password = "zhuzhuainiyo1", "zwh1986729"
		subject = "Python HtmlEmail Test"
		msg = MIMEText("<html><h1>可以点此链接查看详细的测试报告:\n%s<h1><html>" % report_url, "html", "utf-8")
		msg["Subject"] = subject
		smtp = smtplib.SMTP()
		try:
			smtp.connect(smtpserver)
			smtp.login(username, password)
			smtp.sendmail(sender, receiver, msg.as_string())
			print "邮件发送成功"
		except:
			print "邮件发送失败"
		finally:
			smtp.quit()





1.33170775418e+11
99.9932669111
0.00673308887669
