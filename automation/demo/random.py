# -.- coding:utf-8 -.-
import random

def random_str(num):
    """生成随机字符串"""
    try:
        str_tmp = u"""1.2.3.4.5.6.7"""
        str_random = ""
        for i in range(int(num)):
            str_random += (random.choice(str_tmp))

        return str_random
    except:
        raise ValueError("请输入数字长度")
print random_str(5)