#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest,logging, datetime,xmlrunner,time, os, re,random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Test2(unittest.TestCase):
    def test_webin(self):
        self.assertEqual('wow2', 'wow1', 'message:wow==wow!')


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)