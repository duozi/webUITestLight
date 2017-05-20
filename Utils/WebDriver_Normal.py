# -*- coding: UTF-8 -*-
import os
from selenium import webdriver

class WebDriver_Normal(object):
    """
    浏览器相关操作：
    get__driver() 获取浏览器 driver 对象，如果该对象为None就创建一个，创建时默认创建Firefox，可接受一个参数创建别的浏览器
              参数： Firefox Chrome     返回值：driver 对象

    """
    __driver = None
    def __init__(self,browser='Firefox'):
        self.get_driver(browser)

    def get_driver(self, browser='Firefox'):
        """
            获取浏览器 driver 对象。参数： Firefox Chrome
            """
        if self.__driver == None:
            if browser.strip().upper() == 'Firefox'.strip().upper():
                self.__driver = webdriver.Firefox()
            elif browser.strip().upper() == 'Chrome'.strip().upper():
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
                chromedriver = "Utils/chromedriver.exe"
                os.environ["webdriver.chrome.driver"] = chromedriver
                self.__driver = webdriver.Chrome(chrome_options=options)
            self.__driver.maximize_window()
            self.__driver.implicitly_wait(20)
            self.__driver.set_page_load_timeout(30)
        return self.__driver

    def close_driver(self): # 关闭当前
        if self.__driver != None:
            self.__driver.close()
            try:
                if len(self.__driver.window_handles) == 0:
                  self.__driver = None
            except Exception as e:
                print e
                self.__driver = None

    def quit_driver(self): # 关闭所有
        if self.__driver != None:
            self.__driver.quit()
            self.__driver = None
    def clear_all_session(self):
        self.__driver.delete_all_cookies()

if __name__ == '__main__':
    #d = webdriver.Firefox()
    d = webdriver.Chrome()
    d.get('http://www.baidu.com')
    '''
    test = WebDriver_Normal('Chrome')
    print test.get_driver().window_handles
    test.get_driver('Chrome')
    #test.quit_driver()
    test.close_driver()
    test.get_driver('Chrome')
    print test.get_driver().window_handles
    '''
