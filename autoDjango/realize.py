# coding:utf8
__author__ = 'lang.qy'
from django.contrib.auth import authenticate, login


class Realize(object):
    @staticmethod
    def verify(request, query_dict):
        """验证用户名密码"""
        user = authenticate(username=query_dict["user_name"], password=query_dict["pass_word"])
        if user is not None:
            login(request, user)
            return "verify_success"
        else:
            return u"用户名密码错误"
