#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cookielib,time,sys,logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from Utils.HttpAct import HttpAct
from Utils.logger import Logger

class NCPLogin(object):
    def __init__(self, driver):
        self.driver = driver
        #self.driver = webdriver.Chrome()
        self.log = Logger(sys.path[0] + '/logs/autotest.log', logging.DEBUG, logging.DEBUG)

    input_username = (By.ID, 'loginname')
    input_pwd = (By.ID, 'password')
    # input_captcha = (By.ID, 'captcha')
    # btn_login = (By.ID, 'btn-submit')
    btn_login = (By.NAME, '登录')

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

    def userlogin(self, username, userpwd, captcha): #
        input_username = self.driver.find_element(*self.input_username)
        input_username.clear()
        input_username.send_keys(username)

        input_pwd = self.driver.find_element(*self.input_pwd)
        input_pwd.clear()
        input_pwd.send_keys(userpwd)

        input_captcha = self.driver.find_element(*self.input_captcha)
        input_captcha.clear()
        input_captcha.send_keys(captcha)

        btn_login = self.driver.find_element(*self.btn_login)
        btn_login.click()

    def NCPuserlogin(self, username, userpwd):
        input_username = self.driver.find_element(*self.input_username)
        input_username.clear()
        input_username.send_keys(username)

        input_pwd = self.driver.find_element(*self.input_pwd)
        input_pwd.clear()
        input_pwd.send_keys(userpwd)

        btn_login = self.driver.find_element(*self.btn_login)
        btn_login.click()
    def get_loginStatus(self, username, userpwd):
        try:
            self.driver.implicitly_wait(0.5)
            ul = self.driver.find_element(*self.input_username)
            self.log.info(u'当前为未登录状态！马上登录')
            self.NCPuserlogin(username, userpwd)
            time.sleep(1)
        except Exception as e:
            self.log.info(u'当前为登录状态！')
            # flag = ''
        # cj = cookielib.CookieJar()
        # for cookie in self.driver.get_cookies():
        #     print cookie['name']
        #     if cookie['name'] == 'rememberMe':
        #         if self.driver.find_element(*self.input_username)==-1:
        #             print 'test123'
        #             flag = True
        #             break
        # if flag <> True:
        #     # print u'当前为未登录状态！马上登录'
        #     self.log.info(u'当前为未登录状态！马上登录')
        #     self.NCPuserlogin(username, userpwd)
        #     time.sleep(1)
        # else:
        #     # print u'当前为登录状态！'
        #     self.log.info(u'当前为登录状态！')

if __name__ == '__main__':
    ipage = NCPLogin('test')
    ipage.driver.get('http://10.18.12.15:8080/ncp-web/')
    ipage.driver.implicitly_wait(15)
    value = ipage.getcaptcha('http://10.18.12.15:8080/ncp-web/','http://10.18.12.15:8080/ncp-web/pages/login.jsp','http://10.18.12.15:8080/ncp-web/pages/login.jsp')
    # ipage.userlogin('admin','88888888',value)
    ipage.NCPuserlogin('admin', '88888888')
    # cssstr = 'div#leftAccordion >div >div >div[class="panel-title panel-with-icon"]'
    # #cssstr = 'div#leftAccordion >div >div'
    # menus = ipage.driver.find_elements_by_css_selector(cssstr)
    # print len(menus)
    # for menu in menus:
    #     if len(menu.text) > 0:
    #         print menu.text
    #     if menu.text == '07资金管理':
    #         print menu.get_attribute('class'), menu.find_element_by_xpath('..').get_attribute('class')
    #         menu.click()
    #         print menu.get_attribute('class'), menu.find_element_by_xpath('..').get_attribute('class')
    #     if menu.text == '14参数配置':
    #         print 'gogogogogog'
    #         #menu.click()
