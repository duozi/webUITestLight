# -*- coding: utf-8 -*-
import sys
import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from Sys_CBS.PageObj.getElements import LoginElement
# from script.testunite.comm.commFunction import CommFunction
# from Utils.commFunction import CommFunction

class Login(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    comm = ""

    def setUp(self):
        # self.comm = CommFunction()
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        self.driver = webdriver.Chrome(chrome_options=options)
        #self.driver.implicitly_wait(30)
        self.base_url = "http://10.10.45.11:7001/XiaoNiu/logon.html"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_Login(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.implicitly_wait(30)
        #输入用户名
        userlabel,username = self.comm.split_str(self.dict_data["输入值1"])
        driver.find_element(*LoginElement.userEdit).send_keys(username)
        #输入密码
        passwdlabel,passwd = self.comm.split_str(self.dict_data["输入值2"])
        driver.find_element(*LoginElement.passwdEdit).send_keys(passwd)
        #点击提交按扭
        submitdlabel,submit = self.comm.split_str(self.dict_data["输入值3"])
        self.mainWebDr = driver
        print type(self.mainWebDr)
        print "99999999999999999999999999"
        print submitdlabel
        if submitdlabel <>"":
            driver.find_element(*LoginElement.submitButton).click()
        resetlabel,reset = self.comm.split_str(self.dict_data["输入值4"])
        if resetlabel <>"":
            driver.find_element(*LoginElement.resetButton).click()
        if self.is_alert_present():
            driver.switch_to_alert().accept()
        #cc=CommFunction()
        #cc.goto_menu(driver,str1,str2,str3)

        time.sleep(2)

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
    #suite = unittest.TestCase()
    #suite.addTest(Login('test_Login'))
    #results = unittest.TextTestRunner().run(suite)