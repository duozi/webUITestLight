# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from Sys_CBS.PageObj.getElements import LoginElement
import unittest, time, re

class ProductLineCashLoan(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的

    btn_title1 = (By.CSS_SELECTOR, "a[title='基本信息']")
    btn_title2 = (By.CSS_SELECTOR, "a[title='产品分配']")

    def setUp(self):
        self.driver = self.mainWebDr
        self.accept_next_alert = True
        #self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(30)
        self.pub = PublicAct(self.driver)
        # 进入具体菜单
        self.driver.implicitly_wait(6)
        self.pub.goto_menu(self.dict_data)
        self.verificationErrors = []

    def test_ProductLineCashLoan(self):
        driver = self.driver
        if self.dict_data["操作类型"] == '新增现金贷':
            self.logstu.info(self.dict_data["操作类型"])
            self.new_Cash_loan()
        if self.dict_data["操作类型"] == '新增现金贷失败':
            self.logstu.info(self.dict_data["操作类型"])
            self.new_Cash_loan_fail()
        if self.dict_data["操作类型"] == '现金贷产品系列信息修改':
            self.logstu.info(self.dict_data["操作类型"])
            self.Cash_loan_modification()
        if self.dict_data["操作类型"] == '现金贷添加对应商品':
            self.logstu.info(self.dict_data["操作类型"])
            self.Cash_add_products()
        if self.dict_data["操作类型"] == '现金贷删除对应商品':
            self.logstu.info(self.dict_data["操作类型"])
            self.Cash_del_products()
        if self.dict_data["操作类型"] == '现金贷修改配置产品':
            self.logstu.info(self.dict_data["操作类型"])
            self.Cash_products_modification()

    def new_Cash_loan(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'新增')
        ###进入到新增界面
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        try:
            btn = driver.find_element_by_css_selector("input[name='R0F0']")
            Value = btn.get_attribute("value")
        except Exception as e:
            self.logstu.error(e)
        # 输入增新信息
        self.pub.input_values(self.dict_data, 'product', 'right', 'myiframe0')
        # 点击保存按钮
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        if u"该产品名称已被占用，请输入新的名称" == text:
            self.logstu.info(u"该产品名称已被占用,新增失败")
            # 引发一个断言错误
            self.assertEqual(1, 2)
        time.sleep(1)
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'], Value, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)

    def new_Cash_loan_fail(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'新增')
        ###进入到新增界面
        time.sleep(2)
        # 输入增新信息
        self.pub.input_values(self.dict_data, 'product', 'right', 'myiframe0')
        # 点击保存按钮
        self.pub.comeinifm('right')
        #输入信息后点击返回
        self.pub.timeoutBtnClick(u'返回')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        time.sleep(1)

    def Cash_add_products(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        # 查看有多少条数据
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'详情')
        time.sleep(1)
        self.pub.comeinifm('ObjectList','left' )
        self.pub.thread_btn2(driver.find_element(*self.btn_title2 ))
        # 进入产品配置界面
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.thread_btn(u'新增')
        # 进入新增产品串口
        self.pub.comeinifm('ObjectList')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('ObjectList','myiframe0')
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowCheckBox(1)
        self.pub.comeinifm('ObjectList')
        self.pub.thread_btn(u'确定')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)

    def Cash_del_products(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        # 查看有多少条数据
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'详情')
        time.sleep(1)
        # 进入产品配置界面
        self.pub.comeinifm('ObjectList', 'left')
        self.pub.thread_btn2(driver.find_element(*self.btn_title2))
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('ObjectList','right', 'myiframe0')
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.thread_btn(u'删除')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        time.sleep(1)

    def Cash_loan_modification(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        # 查看有多少条数据
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'详情')
        time.sleep(1)
        # 修改内容
        self.pub.input_values(self.dict_data, 'product', 'ObjectList', 'right', 'myiframe0')
        # 保存按钮
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.thread_btn(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)

    def Cash_products_modification(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        # 查看有多少条数据
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'详情')
        time.sleep(1)
        # 进入产品配置界面
        self.pub.comeinifm('ObjectList', 'left')
        self.pub.thread_btn2(driver.find_element(*self.btn_title2))
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('ObjectList','right', 'myiframe0')
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.thread_btn(u'详情')
        self.pub.input_values(self.dict_data, 'product_info', 'ObjectList', 'right', 'myiframe0')
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.timeoutBtnClick(u'保存')
        time.sleep(1)
