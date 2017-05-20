#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cookielib,time,sys,logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from Utils.HttpAct import HttpAct
from Utils.logger import Logger
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException

class CBSLogin(object):
    def __init__(self, driver):
        self.driver = driver
        #self.driver = webdriver.Chrome()
        self.log = Logger(sys.path[0] + '/logs/autotest.log', logging.DEBUG, logging.DEBUG)
        self.verificationErrors = []
        self.accept_next_alert = True

    input_username = (By.NAME, 'UserID')
    input_pwd = (By.NAME, 'Password')
    btn_login = (By.CLASS_NAME, 'button_submit')

    # action
    def getcaptcha(self,loginurl,getimgurl, returnurl):
        myhttp = HttpAct()
        for cookie in self.driver.get_cookies():
            if myhttp.iCookie == '':
                myhttp.iCookie = cookie['name'] + '=' + cookie['value']
            else:  #sid  rememberMe
                myhttp.iCookie = myhttp.iCookie_jar + ',' + cookie['name'] + '=' + cookie['value']
        #myhttp.get_http_request(loginurl)
        myhttp.get_http_request(getimgurl)
        head,body = myhttp.get_http_request(returnurl)
        return body

    def userlogin(self, username, userpwd): #captcha
        self.driver.implicitly_wait(30)
        input_username = self.driver.find_element(*self.input_username)
        input_username.clear()
        input_username.send_keys(username)
        input_pwd = self.driver.find_element(*self.input_pwd)
        input_pwd.clear()
        input_pwd.send_keys(userpwd)
        btn_login = self.driver.find_element(*self.btn_login)
        btn_login.click()
        time.sleep(2)
        if self.is_alert_present():
            try:
                self.driver.switch_to_alert().accept()
            except NoAlertPresentException as e:
                self.log.info(u'没有弹框 \n%s'% e)
        time.sleep(2)
        try:#验证身份登录成功
            self.driver.implicitly_wait(0.5)
            ul = self.driver.find_element(*self.input_username)
            self.log.info(u'登录失败,置为失败')
            self.assertEqual('1', '2')
        except Exception as e:
            self.log.info(u'登录成功！')


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
    # def CBSuserlogin(self, username, userpwd):
    #     input_username = self.driver.find_element(*self.input_username)
    #     input_username.clear()
    #     input_username.send_keys(username)
    #
    #     input_pwd = self.driver.find_element(*self.input_pwd)
    #     input_pwd.clear()
    #     input_pwd.send_keys(userpwd)
    #
    #     btn_login = self.driver.find_element(*self.btn_login)
    #     btn_login.click()

    def get_loginStatus(self, username, userpwd):
        try:
            self.driver.implicitly_wait(0.5)
            ul = self.driver.find_element(*self.input_username)
            self.log.info(u'当前为未登录状态！马上登录')
            self.userlogin(username, userpwd)
            time.sleep(1)
        except Exception as e:
            self.log.info(u'当前为登录状态！')

if __name__ == '__main__':
    ipage = CBSLogin('test')
    ipage.driver.get('http://10.18.12.11:7001/XiaoNiu/')
    ipage.driver.implicitly_wait(15)
    value = ipage.getcaptcha('http://10.18.12.11:7001/XiaoNiu/','http://10.18.12.11:7001/XiaoNiu/logon.html','http://10.18.12.11:7001/XiaoNiu/logon.html')
    ipage.CBSuserlogin('admin', '!000000als')

