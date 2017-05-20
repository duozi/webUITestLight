#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest,logging, datetime,xmlrunner,time, os, re,random
from Sys_NCP.PageObj.NCPTest import NCPTest
from Sys_NCP.PageObj.PageLoginJsp import PageLoginJsp
from Utils.WebDriver_Single import WebDriver_Single
from selenium import webdriver

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class TestLogin(unittest.TestCase):

    def test_login(self):
        # self.driver = WebDriver_Single().get_driver('Chrome')
        # actlogin = PageLoginJsp(self.driver)
        # self.driver.get('http://10.18.12.15:8080/ncp-web/pages/login.jsp')
        # actlogin.userlogin('admin','88888888')
        test = NCPTest()
        test.defaultLoginInfo()
        test.driver.quit()

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)