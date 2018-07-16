# -.- coding:utf-8 -.-
__author__ = 'Administrator'
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


import time,threading_



# 新线程执行的代码:
def loop():
    print 'thread %s is running...' % "11"


    n = 0
    while n < 5:
        n = n + 1
        print 'thread %s >>> %s' % ("22", n)
        time.sleep(1)
    print 'thread %s ended.' % "33"

print 'thread %s is running...' % "44"
t = threading_.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print 'thread %s ended.' % "22"

