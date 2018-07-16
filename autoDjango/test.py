# -.- coding:utf-8 -.-
__author__ = 'lang.qy'
from django.db import connection
curssor = connection.cursor()
print type(curssor)