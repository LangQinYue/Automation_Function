# -.- coding:utf-8 -.-
__author__ = 'Administrator'
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import random

def random_str(len):
    str=""
    for i in range(len):
        num_list = "0123456789"
        str+=(random.choice(num_list))
    return str


print random_str(5)


# print random.randint(0,9)
