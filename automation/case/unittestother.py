#!coding=utf-8
'''
Created on 2016年10月23日

@author: lx-lang.qinyue
'''


import unittest
class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.data = param
        self.verificationErrors = []
    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite
##用法-testcase
class TestOne(ParametrizedTestCase):
    def test_something(self):
        print 'param =', self.param
        self.assertEqual(1, 1)
 
    def test_something_else(self):
        self.assertEqual(2, 2)
''' 
##用法-测试
suite = unittest.TestSuite()
suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=42))
suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=13))
unittest.TextTestRunner(verbosity=2).run(suite)
'''