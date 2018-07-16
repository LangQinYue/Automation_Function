# -.- coding:utf-8 -.-
__author__ = 'lang.qy'


class Action(object):
	@staticmethod
	def click_button():
		return "click button"


ac = Action()

print getattr(Action, "click_button","Error")()
