#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time,sys,logging
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from Utils.logger import Logger
from Sys_CBS.PageObj.lyElementsOperation import PublicAct

class PageIndex(object):
    log = Logger(sys.path[0] + '/logs/autotest.log', logging.DEBUG, logging.DEBUG)
    def __init__(self, driver):
        self.driver = driver
        #self.driver = webdriver.Chrome()
        self.pub = PublicAct(self.driver)

    menus1 = (By.CSS_SELECTOR, 'dl#menu-article >dt')
    menus2 = (By.CSS_SELECTOR, 'dl#menu-article>dd >ul >li >a')
    tabs_li = (By.CSS_SELECTOR, 'ul#min_title_list >li.active >span')

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
                    menutext = menu.text.split(' ')
                    menu_text = menutext[1].split('\n')
                    if menu_text[0] == menustr:
                        if menu.find_element_by_xpath('..').find_element_by_tag_name('dd').get_attribute('style').find('display: block;') == -1:
                            menu.click()
                            return True
                            break
                        else:
                            self.log.debug('一级菜单 %s 已经展开，不用点击了。' % menustr)
                            return True
            except StaleElementReferenceException as e:
                self.log.debug(e)
        self.log.info('未找到菜单 %s' % menustr)
        return False

    # 一级菜单有时候遇到滚动条未达，没显示出来找不到情况
    # def open_menu1(self,menustr):
    #     '''
    #     点击页面左侧一级菜单，显示出二级菜单
    #     :param menustr: 菜单的中文文本
    #     :return:
    #     '''
        # self.log.debug('一一一一 Start Click 一级菜单 %s 一一一一' % menustr)
        # flag = self.open_menu1_base(menustr)
        # if flag == True:
        #     self.log.debug('找到一级菜单 %s' % menustr)
        # if flag == False:
        #     self.log.error('Error: 未找到一级菜单 %s' % menustr)
        # self.log.debug('一一一一 End Click 一级菜单 %s 一一一一' % menustr)
        # return flag

    # 菜单选择
    def goto_menu(self,menu1,menu2,menu3):
        driver = self.driver
        driver.set_page_load_timeout(15)
        menuList = []
        menuList.append(menu1)
        menuList.append(menu2)
        menuList.append(menu3)
        self.log.info('菜单：%s - %s - %s' % (menuList[0], menuList[1], menuList[2]))

        for reclick in range(1, 11):
            for m in range(0, len(menuList)):
                if menuList[m] == '' and m == 0:
                    return
                try:
                    menu_ul = driver.find_element_by_css_selector('ul#ASMenuBar')
                    try:
                        opmenu = menu_ul.find_element_by_link_text(menuList[m])
                    except NoSuchElementException as e:
                        self.log.debug('未找到菜单(%s)，搜索 >> 标志查看是否存在' % (menuList[m]))
                        ActionChains(driver).move_to_element(menu_ul.find_element_by_link_text('>>')).perform()
                        break
                    ActionChains(driver).move_to_element(opmenu).perform()
                    self.log.info('ActionChains MenuName :%s' % opmenu.text)
                    if m >= len(menuList) - 1:
                        opmenu.click()
                        return
                    if menuList[m + 1] == '':
                        opmenu.click()
                        return
                    time.sleep(1)
                except ElementNotVisibleException as e:
                    self.log.debug(e)
                    time.sleep(1)
                except NoSuchElementException as e:
                    self.log.debug(e)
                    wins = driver.window_handles
                    if len(wins) == 1:
                        driver.switch_to_default_content()
                    elif len(wins) > 1:
                        driver.close()
                        self.goLastOneWindow()
                    elif len(wins) == 0:
                        self.log.error('无可供操作的浏览器。')
                    time.sleep(1)
                except WebDriverException as e:
                    self.log.debug(e)
                    time.sleep(1)

    # 用于窗口按钮事件关闭后，切换回打开的窗口
    def goLastOneWindow(self):
        driver = self.driver
        windows = driver.window_handles
        self.log.debug(u'现存窗体：' + ' '.join(windows))
        driver.switch_to_window(windows[len(windows) - 1])
        try:
            self.log.debug(u'跳转到上述窗体列表的最后一个，' + driver.current_window_handle + ' | ' + driver.title)
        except:
            self.log.debug('raise ResponseNotReady()')
            time.sleep(1)
            self.log.debug(u'跳转到上述窗体列表的最后一个，' + driver.current_window_handle + ' | ' + driver.title)

    def open_menu2_base(self, menustr):
        '''
        点击左侧二级菜单
        :param menustr:  菜单的中文文本
        :return:
        '''
        flag = False
        menus2 = self.driver.find_elements(*self.menus2)
        for menu in menus2:
            if menu.text == menustr:
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

    def open_menu2(self,menuOne, menustr):
        self.log.debug('============ Start Click 二级菜单 %s =======' % menustr)
        flag = self.open_menu2_base(menustr)
        if flag == True:
            self.log.debug('找到二级菜单 %s' % menustr)
        if flag == False:
            self.log.error('Error: 未找到二级菜单 %s' % menustr)
            self.assertEqual('1', '2')
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

    # def tabs_act(self, tabname, option):
    #     '''
    #     tab页标签操作，点左侧菜单会生成一个新的tab，含有名称、刷新、删除操作
    #     :param tabname: 需要操作的标签tab名称
    #     :param option:  操作类型， 点击：Click 刷新：Refresh 关闭：Close
    #     :return:
    #     '''
    #     tab1 = None
    #     name = self.try_to_unicode(tabname)
    #     head = self.driver.find_element_by_id('min_title_list')
    #     for tab in head.find_elements_by_tag_name('li'):
    #         if tab.find_element_by_tag_name('span').text.find(name) >= 0:
    #             tab1 = tab
    #             tab.find_element_by_tag_name('i').click()
    #             break
    #     if tab1 == None:
    #         return '未找到 %s' % tabname
    #     else:
    #         return

    def tabcontentcheck(self,checkmenu,linkname):
        '''
        确认tab内容是否正确，check tab中的 a 标签名称，例如查询按钮等
        :param linkname: a标签显示的名称
        :return: 找到则返回 True
        '''
        flag = False
        if linkname <> None and linkname <> '':
            linkname = linkname.strip()
            linkname = self.try_to_unicode(linkname)

            # try:
            self.driver.implicitly_wait(0.5)
            # for j in range(0, 2):  right
            time.sleep(1)
            menus1 ={'商品类型','营销活动定义','电销规则策略','短信推广策略','微信推广策略','渠道管理','区域管理','商户管理','门店管理','银行代码管理','还款文件查询','审批配置'}
            menus2 = {'账务代码定义','流程监控', '综合信息', '代码管理', '第三方接口参数配置','销售人员入职审核','销售人员变更审核'}#,'贷款审批', '商品贷', '现金贷'
            menus3 = {'流程阶段审核要点'}
            if checkmenu in menus1:
                self.pub.comeinifm('right', 'rightup')
            elif checkmenu in menus2:
                self.pub.comeinifm('left', 'frameright')
            elif checkmenu in menus3:
                self.pub.comeinifm('right', 'frameleft')
            else:
                self.pub.comeinifm('right', 'frameright')
            try:
                self.driver.implicitly_wait(0.5)
                tagas = self.driver.find_elements_by_tag_name('a')
            except Exception as e:
                self.log.info('页面不存在a标签.%s' % e)
            if len(tagas) > 0:
                for i in tagas:
                    self.log.info("check tab a, current a|search a: %s|%s" % (i.text.strip(), linkname))
                    if i.text.strip() == linkname:
                        self.driver.switch_to_default_content()
                        flag = True
                        break
                    else:
                        atext = i.text.split(' ')
                        if len(atext) > 1:
                            if atext[1].strip() == linkname:
                                self.driver.switch_to_default_content()
                                flag = True
                                break
            try:
                self.driver.implicitly_wait(0.5)
                spans = self.driver.find_elements_by_tag_name('span')
            except Exception as e:
                self.log.info('页面不存在span标签.%s' % e)
            if len(spans) > 0:
                for span in spans:
                    self.log.info("check tab a, current a|search a: %s|%s" % (span.text.strip(), linkname))
                    if span.text.strip() == linkname:
                        self.driver.switch_to_default_content()
                        flag = True
                        break

            try:
                self.driver.implicitly_wait(0.5)
                ths = self.driver.find_elements_by_tag_name('th')
            except Exception as e:
                self.log.info('页面不存在th标签.%s' % e)
            if len(ths) > 0:
                for th in ths:
                    self.log.info("check tab a, current a|search a: %s|%s" % (th.text.strip(), linkname))
                    if th.text.strip() == linkname:
                        self.driver.switch_to_default_content()
                        flag = True
                        break
            try:
                self.driver.implicitly_wait(0.5)
                buttons = self.driver.find_elements_by_tag_name('button')
            except Exception as e:
                self.log.info('页面不存在button标签.%s' % e)
            if len(buttons) > 0:
                for button in buttons:
                    self.log.info("check tab a, current a|search a: %s|%s" % (button.text.strip(), linkname))
                    if button.text.strip() == linkname:
                        self.driver.switch_to_default_content()
                        flag = True
                        break
                    else:
                        buttontext = button.text.split(' ')
                        if len(buttontext) > 1:
                            print buttontext[1]
                            if buttontext[1].strip() == linkname:
                                self.driver.switch_to_default_content()
                                flag = True
                                break

            self.driver.switch_to_default_content()
            if flag == True:
                self.driver.switch_to_default_content()
                self.log.info('已查找到：%s.' % linkname)
                return flag
                # break
            else:
                self.log.info('页面未找到：%s.' % (linkname))
                flag = False
                self.assertEqual('1', '2')

    def try_to_unicode(self, value):
        try:
            value = unicode(value, 'utf8')
        except Exception as e:
            # print e
            pass
        return value


if __name__ == '__main__':
    ipage = PageIndex('test')
    print ipage.getcaptcha('http://10.18.12.61:8091/xncar/','http://10.18.12.61:8091/xncar/Login!captcha.action','http://10.18.12.61:8091/xncar/Login!getCaptcha.action')