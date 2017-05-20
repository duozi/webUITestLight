#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from Utils.HttpAct import HttpAct

class PageLogin(object):
    def __init__(self, driver):
        self.driver = driver
        #self.driver = webdriver.Chrome()

    input_username = (By.ID, 'user_code')
    input_pwd = (By.ID, 'login_pwd')
    input_captcha = (By.ID, 'captcha')
    btn_login = (By.ID, 'btn-submit')

    # action
    def getcaptcha(self,loginurl,getimgurl, returnurl):
        myhttp = HttpAct()
        for cookie in self.driver.get_cookies():
            if myhttp.iCookie == '':
                myhttp.iCookie = cookie['name'] + '=' + cookie['value']
            else:
                myhttp.iCookie = myhttp.iCookie_jar + ',' + cookie['name'] + '=' + cookie['value']
        #myhttp.get_http_request(loginurl)
        myhttp.get_http_request(getimgurl)
        head,body = myhttp.get_http_request(returnurl)
        return body

    def userlogin(self, username, userpwd, captcha):
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

if __name__ == '__main__':
    ipage = PageLogin('test')
    ipage.driver.get('http://10.18.12.61:8091/xncar/')
    ipage.driver.implicitly_wait(15)
    value = ipage.getcaptcha('http://10.18.12.61:8091/xncar/','http://10.18.12.61:8091/xncar/Login!captcha.action','http://10.18.12.61:8091/xncar/Login!getCaptcha.action')
    ipage.userlogin('admin','888888',value)
    cssstr = 'div#leftAccordion >div >div >div[class="panel-title panel-with-icon"]'
    #cssstr = 'div#leftAccordion >div >div'
    menus = ipage.driver.find_elements_by_css_selector(cssstr)
    print len(menus)
    for menu in menus:
        if len(menu.text) > 0:
            print menu.text
        if menu.text == '07资金管理':
            print menu.get_attribute('class'), menu.find_element_by_xpath('..').get_attribute('class')
            menu.click()
            print menu.get_attribute('class'), menu.find_element_by_xpath('..').get_attribute('class')
        if menu.text == '14参数配置':
            print 'gogogogogog'
            #menu.click()

