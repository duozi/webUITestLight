# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
import unittest, time, re

class AfterLoanSalesReturnApprove(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    row =""          #接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象
    actdb = None  # 接收main脚本传送的mysql处理类对象

    #页面控件元素别
    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_AfterLoanRefundApprove(self):
        driver = self.driver
        #driver =webdriver.Firefox()

        #确认是否需要登录
        if (self.dict_data["登录用户"] <> "" and self.dict_data["登录密码"] <> ""):
            self.comm.goto_menu(driver,self.row)
        #获取操作类型
        opt = self.dict_data["操作类型"].split("|")
        print opt[0]
        #中间按扭的操作
        if opt[0] == u'审批通过':
            self.logstu.info("开始审批通过操作")
            self.approve_pass()
        if opt[0] == u'审批未通过':
            self.logstu.info("开始审批未通过操作")
            self.approve_nopass()



    #审批通过操作
    def approve_pass(self):
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        if self.pub.is_table_getRowsCount_exist(self.row,self.comm) > 0:
            #选择第一行数据
            self.pub.table_RowClick(1)
            self.pub.comeinifm('right')
            self.pub.table_BtnClick(u'审批通过')
            resluttext = self.pub.is_alert_and_close_and_get_text2()
            self.logstu.info(resluttext)
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (
                self.actdb.casetitle_cn['执行结果'], resluttext, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)


    #审批未通过操作
    def approve_nopass(self):
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        mainhs = self.driver.current_window_handle
        if self.pub.is_table_getRowsCount_exist(self.row,self.comm) > 0:
            #选择第一行数据
            self.pub.table_RowClick(1)
            self.pub.comeinifm('right')
            oldhs = self.driver.window_handles
            self.driver.set_page_load_timeout(1)
            try:
                self.pub.table_BtnClick(u'审批未通过')
            except TimeoutException as e:
                print e
            #点击详情后直接跳转到新窗口
            alertname1 = self.pub.is_alert_and_close_and_get_text()
            if alertname1 == False :
                self.pub.goNewWindow(oldhs)
                self.pub.comeinifm('ObjectList','myiframe0')
                self.pub.setEditTableValues(self.dict_data,'ObjectList','myiframe0')
                self.pub.comeinifm('ObjectList')
                self.pub.table_BtnClick(u'确定')
                self.pub.is_alert_and_close_and_get_text() #第一个弹出框直接关闭
                self.driver.switch_to_window(mainhs)
                resluttext = self.pub.is_alert_and_close_and_get_text2()
                self.logstu.info(resluttext)
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (
                    self.actdb.casetitle_cn['执行结果'], resluttext, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
            else:
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (
                    self.actdb.casetitle_cn['执行结果'], alertname1, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)

    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

