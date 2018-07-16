#!coding=utf-8
'''
Created on 2016年10月23日

@author: lx-lang.qinyue
'''

import sys

import json
import unittest
from os import path
from case_type import Operation
from automation.public.action import ParseStep


class KeyWord(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []

    def action(self, data):
        self.parse = ParseStep(data)
        self.verificationErrors.extend(self.parse.run_step())

    @staticmethod
    def getTestFunc(data):
        def func(self):
            self.action(data)

        return func

    def tearDown(self):
        print "-" * 40, u"用例运行完成", "-" * 40
        self.assertEqual([], self.verificationErrors)
def factory_cases():
    config_path = path.join(path.dirname(path.abspath(__file__)), "config.json")
    if path.exists(config_path):
        with open(config_path) as f:            
            f = json.loads(f.read())
            op = Operation()
            case_list = op.choose(f)
            
        for data in case_list:
            setattr(KeyWord, 'test_name:%s' % data["name"], KeyWord.getTestFunc(data))

    else:
        raise IOError("config not found")


factory_cases()
        
