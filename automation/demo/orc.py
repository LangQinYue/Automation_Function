__author__ = 'vip'
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import cx_Oracle
connectType = 'SID'
connectData = 'test'
address = '172.16.200.72'
port = '1521'
userName = 'poseidon1'
passWord = '123456'

dsn = cx_Oracle.makedsn(address, port, connectData)

con = cx_Oracle.connect(userName, passWord, dsn)
print con.version


# if str(connectType) == u'SID':
#     dsn = cx_Oracle.makedsn(address, port, connectData)
#     print dsn
#     con = cx_Oracle.connect(userName, passWord, dsn)
#     print con.verison
# elif str(connectType) == u'ServerName':
#     dsn = str(address) + ":" + str(port) + "/" + str(connectData)
#     con = cx_Oracle.connect(userName, passWord, dsn)