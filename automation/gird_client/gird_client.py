# -.- coding:utf-8 -.-
__author__ = 'lang.qy'
import os
from os import path


class GirdClient(object):
	def __init__(self, server_ip, server_port):
		"""
		:param server_ip:remote server ip
		:param server_port:remote server port
		:return:path
		"""
		self.server_ip = server_ip
		self.server_port = server_port

	def gird_path(self):
		file_path = path.join(path.dirname(path.abspath(__file__)), "selenium-server-standalone-2.48.2.jar")
		if path.exists(file_path):
			full_path = "java -jar {} -role webdriver -hub http://{}/grid/register -port {}".format(file_path, self.server_ip,
			                                                                                        self.server_port)
			return full_path
		else:
			raise OSError("File Path Error")

	def run_gird(self):
		try:
			os.system(self.gird_path())
		except Exception as e:
			raise RuntimeError(e)


if __name__ == "__main__":
	ip, port = "192.168.80.141:4444", "5555"
	GirdClient(ip, port).run_gird()
