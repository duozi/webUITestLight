#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium.webdriver.common.by import By

class PageLoginJsp(object):
    def __init__(self, driver):
        self.driver = driver

    input_username = (By.ID, 'loginname')
    input_pwd = (By.ID, 'password')
    btn_login = (By.CSS_SELECTOR, 'input[name="登录"][type="submit"]')
    btn_cancel = (By.CSS_SELECTOR, 'input[name="取消"][type="reset"]')

    # action
    def userlogin(self, username, userpwd):
        input_username = self.driver.find_element(*self.input_username)
        input_username.clear()
        input_username.send_keys(username)
        input_pwd = self.driver.find_element(*self.input_pwd)
        input_pwd.clear()
        input_pwd.send_keys(userpwd)
        btn_login = self.driver.find_element(*self.btn_login)
        btn_login.click()