#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time,sys,logging
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from Utils.logger import Logger
class PageIndex(object):
    log = Logger(sys.path[0] + '/logs/autotest.log', logging.DEBUG, logging.DEBUG)
    def __init__(self, driver):
        self.driver = driver
        #self.driver = webdriver.Chrome()

    menus1 = (By.CSS_SELECTOR, 'div#leftAccordion >div >div >div[class="panel-title panel-with-icon"]')
    #menus2 = (By.CSS_SELECTOR, 'ul#tree >li >div >span.tree-title')
    menus2 = (By.CSS_SELECTOR, 'ul#tree >li')
    menus3 = (By.CSS_SELECTOR, 'ul#tree >li >ul >li >div >span.tree-title')

    tabs_li = (By.CSS_SELECTOR, 'ul.tabs >li')

    # 菜单div的滚动条操作
    def menu_scrollTop(self, position='bottom'):
        if position.lower() == 'bottom' or position.lower() != 'top':
            # 将页面滚动条拖到底部
            js = "document.getElementById('leftAccordion').parentElement.scrollTop=10000"
            self.driver.execute_script(js)
            time.sleep(1)
        if position.lower() == 'top':
            # 将页面滚动条拖到顶部
            js = "document.getElementById('leftAccordion').parentElement.scrollTop=0"
            self.driver.execute_script(js)
            time.sleep(1)

    # 一级菜单操作
    def open_menu1_base(self,menustr):
        time.sleep(1)
        for j in range(6):
            menus1 = self.driver.find_elements(*self.menus1)
            try:
                for menu in menus1:
                    if menu.text == menustr:
                        self.log.debug('找到一级菜单 %s' % menustr)
                        if menu.find_element_by_xpath('..').get_attribute('class').find('selected') == -1:
                            menu.click()
                            try:
                                ul = menu.find_element_by_xpath('../..').find_element_by_css_selector('div >ul')
                                listr = ''
                                for i in ul.find_elements_by_css_selector('li'):
                                    if listr != '':
                                        listr = listr +' | '+ i.text
                                    else:
                                        listr = i.text
                                self.log.debug('%s 对应的二级菜单为：%s' % (menustr, listr))
                                if listr != '':
                                    return True
                                self.driver.refresh()
                                time.sleep(1)
                            except Exception as e:
                                self.log.debug(e)
                                self.driver.refresh()
                                time.sleep(1)
                                break
                        else:
                            self.log.debug('一级菜单 %s 已经展开，不用点击了。' % menustr)
                            return True
            except StaleElementReferenceException as e:
                self.log.debug(e)
        self.log.info('未找到菜单 %s' % menustr)
        return False

    # 一级菜单有时候遇到滚动条未达，没显示出来找不到情况
    def open_menu1(self,menustr):
        '''
        点击页面左侧一级菜单，显示出二级菜单
        :param menustr: 菜单的中文文本
        :return:
        '''
        self.log.debug('一一一一 Start Click 一级菜单 %s 一一一一' % menustr)
        flag = self.open_menu1_base(menustr)
        if flag == True:
            self.log.debug('找到一级菜单 %s' % menustr)
        if flag == False:
            self.log.debug('未找到一级菜单 %s, 将页面滚动条拖到底部再次尝试' % menustr)
            # 将页面滚动条拖到底部
            self.menu_scrollTop('bottom')
            flag = self.open_menu1_base(menustr)
            if flag == True:
                self.log.debug('滚动到底部后找到一级菜单 %s' % menustr)
        if flag == False:
            self.log.debug('未找到一级菜单 %s, 将页面滚动条拖到顶部再次尝试' % menustr)
            # 将页面滚动条拖到顶部
            self.menu_scrollTop('top')
            flag = self.open_menu1_base(menustr)
            if flag == True:
                self.log.debug('滚动到顶部后找到一级菜单 %s' % menustr)
        if flag == False:
            self.log.error('Error: 未找到一级菜单 %s' % menustr)
        self.log.debug('一一一一 End Click 一级菜单 %s 一一一一' % menustr)
        return flag

    def open_menu2_base(self, menustr):
        '''
        点击左侧二级菜单
        :param menustr:  菜单的中文文本
        :return:
        '''
        flag = False
        menus2 = self.driver.find_elements(*self.menus2)
        for menu in menus2:
            if menu.find_element_by_css_selector('div >span.tree-title').text == menustr:
                self.log.debug('找到二级菜单 %s' % menustr)
                try:
                    self.driver.implicitly_wait(0.5)
                    ul = menu.find_element_by_tag_name('ul')
                    for i in range(0,5):
                        if ul.get_attribute('style')!='display: none;':
                            break
                        menu.click()
                        time.sleep(0.5)
                except Exception as e:
                    self.log.info('二级菜单 %s 下没有三级菜单. \n%s' % (menustr,e))
                    menu.click()
                    time.sleep(0.5)
                    if self.tab_is_exist(menustr) == False:
                        self.log.debug('打开tab %s 失败, 调整滚动条位置后再尝试一次。' % menustr)
                        self.menu_scrollTop('bottom')
                        menu.click()
                    if self.tab_is_exist(menustr) == False:
                        self.log.debug('打开tab %s 失败, 调整滚动条位置后再尝试一次。' % menustr)
                        self.menu_scrollTop('top')
                        menu.click()
                finally:
                    self.driver.implicitly_wait(20)
                    flag = True
                    break
        return flag

    def open_menu2(self, menustr):
        self.log.debug('============ Start Click 二级菜单 %s =======' % menustr)
        flag = self.open_menu2_base(menustr)
        if flag == True:
            self.log.debug('找到二级菜单 %s' % menustr)
        if flag == False:
            self.log.debug('未找到二级菜单 %s, 将页面滚动条拖到底部再次尝试' % menustr)
            # 将页面滚动条拖到底部
            self.menu_scrollTop('bottom')
            flag = self.open_menu1_base(menustr)
            if flag == True:
                self.log.debug('滚动到底部后找到二级菜单 %s' % menustr)
        if flag == False:
            self.log.debug('未找到二级菜单 %s, 将页面滚动条拖到顶部再次尝试' % menustr)
            # 将页面滚动条拖到顶部
            self.menu_scrollTop('top')
            flag = self.open_menu1_base(menustr)
            if flag == True:
                self.log.debug('滚动到顶部后找到二级菜单 %s' % menustr)
        if flag == False:
            self.log.error('Error: 未找到二级菜单 %s' % menustr)
        self.log.debug('============ End Click 二级菜单 %s =======' % menustr)

    def open_menu3(self, menustr):
        '''
        点击左侧三级菜单
        :param menustr:  菜单的中文文本
        :return:
        '''
        self.log.debug('三三三三三三三三三三三三 Start Click 三级菜单 %s 三三三三三三三三三三三三' % menustr)
        time.sleep(0.5)
        menus3 = self.driver.find_elements(*self.menus3)
        for menu in menus3:
            if menu.text == menustr:
                self.log.debug('找到三级菜单 %s' % menustr)
                menu.click()
                time.sleep(0.5)
                if self.tab_is_exist(menustr) == False:
                    self.log.debug('打开tab %s 失败, 调整滚动条位置后再尝试一次。' % menustr)
                    self.menu_scrollTop('bottom')
                    menu.click()
                if self.tab_is_exist(menustr) == False:
                    self.log.debug('打开tab %s 失败, 调整滚动条位置后再尝试一次。' % menustr)
                    self.menu_scrollTop('top')
                    menu.click()
                return True
        self.log.error('Error： 未找到三级菜单 %s' % menustr)
        self.log.debug('三三三三三三三三三三三三 End Click 三级菜单 %s 三三三三三三三三三三三三' % menustr)


    def tab_is_exist(self, tabname):
        '''
        判断 tab 是否存在， 不存在返回False
        :param tabname:
        :return:
        '''
        for j in range(0,5):
            time.sleep(0.5)
            for i in self.driver.find_elements(*self.tabs_li):
                if i.text == tabname:
                    return True
            time.sleep(1)
        return False

    def tabs_act(self, tabname, option):
        '''
        tab页标签操作，点左侧菜单会生成一个新的tab，含有名称、刷新、删除操作
        :param tabname: 需要操作的标签tab名称
        :param option:  操作类型， 点击：Click 刷新：Refresh 关闭：Close
        :return:
        '''
        tab = None
        for i in self.driver.find_elements(*self.tabs_li):
            if i.text == tabname:
                tab = i
                if option.lower() == 'Click'.lower():
                    i.click()
                elif option.lower() == 'Refresh'.lower():
                    i.find_element_by_css_selector('a.icon-mini-refresh').click()
                elif option.lower() == 'Close'.lower():
                    i.find_element_by_css_selector('a.tabs-close').click()
        if tab == None:
            return '未找到 %s' % tabname
        else:
            return

    def tabcontentcheck(self, linkname):
        '''
        确认tab内容是否正确，check tab中的 a 标签名称，例如查询按钮等
        :param linkname: a标签显示的名称
        :return: 找到则返回 True
        '''
        for j in range(0,5):
            time.sleep(1)
            ifreams = self.driver.find_elements_by_css_selector('iframe')
            for ifr in ifreams:
                if ifr.is_displayed() == True:
                    self.driver.switch_to_frame(ifr)
                    break
            tagas = self.driver.find_elements_by_tag_name('a')
            for i in tagas:
                self.log.info("check tab a, current a|search a: %s|%s"%(i.text,linkname))
                if i.text == linkname:
                    self.driver.switch_to_default_content()
                    return True
            self.driver.switch_to_default_content()
        return False


if __name__ == '__main__':
    ipage = PageIndex('test')
    print ipage.getcaptcha('http://10.18.12.61:8091/xncar/','http://10.18.12.61:8091/xncar/Login!captcha.action','http://10.18.12.61:8091/xncar/Login!getCaptcha.action')