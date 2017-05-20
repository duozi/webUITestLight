#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import time,os
from Sys_CBS.PageObj.commFunction import CommFunction
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By

class ChannelRetailStoreStore(unittest.TestCase):
    '''渠道管理  商户门店管理  门店管理'''
    # 产品管理-商品类型：增删改查
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
    logstu = ""  # 接收main脚本传递来的写log的对象

    link_a = (By.TAG_NAME, 'a')  # 门店详情  关联产品  关联销售人员
    check_pro = (By.CSS_SELECTOR, 'input[type="checkbox"]')
    gl_pro_savebtn = (By.ID, 'buttonmiddletd21')
    def link_a_go(self, aName):
        alla = self.driver.find_elements(*self.link_a)
        for onea in alla:
            if self.pub.all_type_to_encode(onea.text) == self.pub.all_type_to_encode(aName):
                onea.click()
                return
        raise Exception('未找到按钮：' + self.pub.all_type_to_encode(aName))
    def check_pro_sel(self, selin):
        checklist = self.driver.find_elements(*self.check_pro)
        for num in selin.split('+'):
            checklist[int(num) - 1].click()
    def gl_pro_savebtn_click(self):
        self.driver.find_element(*self.gl_pro_savebtn).click()

    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.logstu.info(self.pub.all_type_to_encode(self.dict_data["案例名称"]) + '---' + self.pub.all_type_to_encode(
            self.dict_data["案例详情"]))
        self.logstu.debug(self.mainWebDr)
        self.logstu.debug(self.driver)
        # 进入具体菜单项
        self.pub.comeinifm()
        self.pub.goto_menu(self.dict_data)

    # 测试类
    def test_RetailStoreApply(self):
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '激活':
            self.logstu.info(u'激活')
            self.activatedStore()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '关联销售人员':
            self.logstu.info(u'关联销售人员')
            self.relationSales()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '关联产品':
            self.logstu.info(u'关联产品')
            self.relationProduct()


    # 查询操作
    def selectStore(self):
        driver = self.driver
        self.pub.comeinifm('right')
        # self.pub.select_sets(self.dict_data)
        # self.pub.select_btn(u'查询')
        self.pub.selectAutoSets(self.dict_data)
        driver.switch_to_default_content()

    # 激活
    def activatedStore(self):
        driver = self.driver
        self.selectStore()

        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)

        # 点击激活按钮
        self.pub.comeinifm('right')
        self.pub.base_thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])
        self.logstu.debug(self.pub.is_alert_and_close_and_get_text2()) #确定要激活门店：men07141436
        for i in range(0,6):
            if self.pub.is_alert_present2():
                try:
                    alerttext = self.pub.is_alert_and_close_and_get_text2()
                    self.logstu.debug(alerttext)
                    break
                except NoAlertPresentException as e:
                    self.logstu.debug(e)
                    self.logstu.debug('为捕获到激活确认弹窗，等待0.5秒后重试')
                    time.sleep(0.5)

        # check
        time.sleep(3)
        okrl = self.pub.all_type_to_encode(self.dict_data["预期结果"])
        for i in range(0,10):
            self.pub.comeinifm('right', 'myiframe0')
            rult = self.pub.table_getValue2(1, '门店状态')
            self.logstu.debug('门店状态 : ' + rult + ' | 预期结果：' + okrl)
            if rult == okrl:
                break
            self.logstu.debug('表格查询到的数据和预期不一致，重试'+ str(i+1)+'次')
            time.sleep(0.5)
        self.logstu.debug(u'执行结果【' + self.pub.all_type_to_unicode(rult) + u'】写入testcals.xls，\r\n预期结果为：' + self.pub.all_type_to_unicode(okrl))
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], rult, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        self.assertEqual(rult,okrl, '预期结果：' + okrl + '  | 实际结果：' + rult)

    # 关联销售人员
    def relationSales(self):
        driver = self.driver
        self.selectStore()
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)
        # 点击详情按钮
        self.pub.comeinifm('right')
        oldhs = driver.window_handles
        driver.set_page_load_timeout(1)
        try:
            self.pub.thread_btn('详情')
        except TimeoutException as e:
            self.logstu.debug(e)
        driver.set_page_load_timeout(30)
        self.pub.goNewWindow(oldhs)

        self.pub.comeinifm('ObjectList')
        self.link_a_go('关联销售人员')
        self.pub.comeinifm('ObjectList', 'tab_T01_iframe_TS2', 'myiframe0')
        old_count = self.pub.table_getRowsCount()
        self.pub.comeinifm('ObjectList','tab_T01_iframe_TS2')
        self.pub.thread_btn('新增')

        #self.pub.setEditTableValues(self.dict_data, 'ObjectList', 'tab_T01_iframe_TS2', 'myiframe0')
        self.pub.setEditTableValueFast(self.dict_data, 'ObjectList', 'tab_T01_iframe_TS2', 'myiframe0')
        self.pub.comeinifm('ObjectList', 'tab_T01_iframe_TS2')
        self.pub.thread_btn(u'保存')
        if self.pub.is_alert_present(self.driver):
            try:
                alerttext = self.pub.close_alert_and_get_its_text()
                self.logstu.debug(alerttext)
            except NoAlertPresentException as e:
                self.logstu.debug(e)
        else:
            self.pub.thread_btn(u'返回')

        self.pub.comeinifm('ObjectList', 'tab_T01_iframe_TS2', 'myiframe0')
        new_count = self.pub.table_getRowsCount()
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], '关联销售人员，关联前 ' + str(old_count) + ' 个，关联后 ' + str(new_count), self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        self.pub.winClose()
        self.assertEqual(old_count, new_count - 1, '关联销售人员，关联前有销售人员 ' + str(old_count) + ' 个，关联后有 ' + str(new_count))

    # 关联产品
    def relationProduct(self):
        driver = self.driver
        self.selectStore()
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)
        # 点击详情按钮
        self.pub.comeinifm('right')
        oldhs = driver.window_handles
        driver.set_page_load_timeout(1)
        try:
            self.pub.thread_btn('详情')
        except TimeoutException as e:
            self.logstu.debug(e)
        driver.set_page_load_timeout(30)
        self.pub.goNewWindow(oldhs)

        self.pub.comeinifm('ObjectList')
        self.link_a_go('关联产品')
        self.pub.comeinifm('ObjectList', 'tab_T01_iframe_TS1', 'myiframe0')
        old_count = self.pub.table_getRowsCount()
        oldlist = []
        if old_count > 0:
            for c in range(1, old_count + 1):
                oldlist.append(self.pub.table_getValue2(c,'产品系列'))
        self.pub.comeinifm('ObjectList', 'tab_T01_iframe_TS1')

        oldhs2 = driver.window_handles
        driver.set_page_load_timeout(1)
        try:
            self.pub.thread_btn('新增')
        except TimeoutException as e:
            self.logstu.debug(e)
        driver.set_page_load_timeout(30)
        self.pub.goNewWindow(oldhs2)

        self.pub.comeinifm('ObjectList')
        self.check_pro_sel(self.pub.all_type_to_encode(self.dict_data['输入值1']).split('|')[1])
        self.pub.comeinifm('ObjectList')
        #self.pub.thread_btn('保存')
        self.gl_pro_savebtn_click()
        driver.switch_to_default_content()
        self.pub.winClose()

        self.pub.comeinifm('ObjectList', 'tab_T01_iframe_TS1', 'myiframe0')
        for i in range(1,11):
            new_count = self.pub.table_getRowsCount()
            if new_count != old_count:
                break
            time.sleep(0.5)
        newlist = []
        if new_count > 0:
            for c in range(1, new_count + 1):
                newlist.append(self.pub.table_getValue2(c, '产品系列'))

        driver.switch_to_default_content()
        self.pub.winClose()

