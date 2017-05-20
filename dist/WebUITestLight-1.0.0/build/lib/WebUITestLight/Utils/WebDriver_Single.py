# -*- coding: UTF-8 -*-
import os
from selenium import webdriver

class WebDriver_Single(object):
    driver = None;
    # 单例模式创建driver
    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super(WebDriver_Single, cls).__new__(cls)
        return cls.instance

    def get_driver(self, browser='Firefox'):
        if self.driver == None:
            if browser.strip().upper() == 'Firefox'.strip().upper():
                self.driver = webdriver.Firefox()
            elif browser.strip().upper() == 'Chrome'.strip().upper():
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
                chromedriver = "Utils/chromedriver.exe"
                os.environ["webdriver.chrome.driver"] = chromedriver
                self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        return self.driver