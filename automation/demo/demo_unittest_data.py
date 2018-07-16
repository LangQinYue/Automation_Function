#!coding=utf-8
'''
Created on 2016年10月23日

@author: lx-lang.qinyue
'''

import unittest  
  
l = [["foo", "a", "a",], ["bar", "a", "a"], ["lee", "b", "b"]]  
  
class TestSequenceMeta(type):  
    def __new__(mcs, name, bases, dict):  
  
        def gen_test(a, b):  
            def test(self):  
                self.assertEqual(a, b)  
            return test  
  
        for tname, a, b in l:  
            test_name = "test_%s" % tname  
            dict[test_name] = gen_test(a,b)  
        return type.__new__(mcs, name, bases, dict)  
  
class TestSequence(unittest.TestCase):  
    __metaclass__ = TestSequenceMeta  
  
if __name__ == '__main__':  
    unittest.main()