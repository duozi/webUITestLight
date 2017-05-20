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

class AfterLoanPaymentAgreementUpload(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
    #页面控件元素别
    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_AfterLoanPaymentAgreementUpload(self):
        driver = self.driver
        #driver =webdriver.Firefox()

        #确认是否需要登录
        if (self.dict_data["登录用户"] <> "" and self.dict_data["登录密码"] <> ""):
            self.comm.goto_menu(driver,self.row)
        #获取操作类型
        opt = self.dict_data["操作类型"].split("|")
        #中间按扭的操作
        if opt[0] == u'期款豁免协议上传':
            self.payment_upload()


    #期款豁免协议上传
    def payment_upload(self):
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        if self.pub.is_table_getRowsCount_exist(self.row,self.comm) > 0 :
            #选择第一行数据
            self.pub.table_RowClick(1)
            self.pub.comeinifm('right')
            oldhs = self.driver.window_handles
            self.driver.set_page_load_timeout(1)
            try:
                self.pub.table_BtnClick(u'期款豁免协议上传')
            except TimeoutException as e:
                print e
            self.pub.goNewWindow(oldhs)
            self.pub.comeinifm('ObjectList')
            upload_rult = self.pub.all_type_to_encode(self.pub.uploadfile('2.jpg'))
            self.assertNotEqual(upload_rult.find('上传文件成功'), -1)
            self.driver.switch_to_default_content()
            self.pub.winClose() # 关闭上传文件弹窗
            self.pub.comeinifm('ObjectList')
            self.pub.table_BtnClick(u'确认')
            resluttext = self.pub.is_alert_and_close_and_get_text2()
            self.logstu.info(resluttext)
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'], resluttext, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)

   #审批未通过操作
    def apply_return(self):
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        #选择第一行数据
        self.pub.table_RowClick(1)
        self.pub.comeinifm('right')
        oldhs = self.driver.window_handles
        self.driver.set_page_load_timeout(1)
        try:
            self.pub.table_BtnClick(u'申请退保')
        except TimeoutException as e:
            print e
        #点击详情后直接跳转到新窗口
        alertname1 = self.pub.is_alert_and_close_and_get_text()
        if alertname1 == False :
            self.pub.goNewWindow(oldhs)
            #self.pub.goNameWindow('小牛消费金融业务管理系统')
            self.pub.setEditTableValues(self.dict_data,'ObjectList','myiframe0')
            self.pub.comeinifm('ObjectList')
            oldhs = self.driver.window_handles
            self.driver.set_page_load_timeout(1)
            try:
                self.pub.table_BtnClick('上传附件')
            except TimeoutException as e:
                print e
            self.pub.goNewWindow(oldhs)
            self.pub.comeinifm('ObjectList')
            upload_rult = self.pub.all_type_to_encode(self.pub.uploadfile('2.jpg'))
            self.assertNotEqual(upload_rult.find('上传文件成功'), -1)
            self.driver.switch_to_default_content()
            self.pub.winClose() # 关闭上传文件弹窗
            self.pub.comeinifm('ObjectList')
            self.pub.table_BtnClick(u'确认')
            resluttext = self.pub.is_alert_and_close_and_get_text2()
            self.logstu.info(resluttext)
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'], resluttext, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
        else:
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'], alertname1, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
        self.pub.winClose()

    #代扣账号变更
    def acct_reset(self):
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        #选择第一行数据
        self.pub.table_RowClick(1)
        self.pub.comeinifm('right')
        oldhs = self.driver.window_handles
        self.driver.set_page_load_timeout(1)
        try:
            self.pub.table_BtnClick(u'代扣账号变更')
        except TimeoutException as e:
            print e
        #点击详情后直接跳转到新窗口
        if self.get_alert_presentname() == False :
            self.pub.goNewWindow(oldhs)
            #self.pub.goNameWindow('小牛消费金融业务管理系统')
            self.pub.setEditTableValues(self.dict_data,'ObjectList','myiframe0')
            self.pub.comeinifm('ObjectList')
            print "333333333444444444444444444444444"
            oldhs = self.driver.window_handles
            self.driver.set_page_load_timeout(1)
            try:
                self.pub.table_BtnClick(u'确认变更')
            except TimeoutException as e:
                print e
            time.sleep(0.5)
            self.pub.is_alert_and_close_and_get_text()
            self.pub.goNewWindow(oldhs)
            self.pub.comeinifm('ObjectList')
            upload_rult = self.pub.all_type_to_encode(self.pub.uploadfile('2.jpg'))
            self.assertNotEqual(upload_rult.find('上传文件成功'), -1)
            self.driver.switch_to_default_content()
            self.pub.winClose() # 关闭上传文件弹窗
            self.pub.comeinifm('ObjectList')
            self.pub.table_BtnClick(u'确认')
            self.pub.is_alert_and_close_and_get_text()
            self.pub.winClose()
            self.pub.winClose()
        else:
            self.pub.is_alert_and_close_and_get_text()

    #提前还款申请
    def advance_apply(self):
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        #选择第一行数据
        self.pub.table_RowClick(1)
        self.pub.comeinifm('right')
        oldhs = self.driver.window_handles
        self.driver.set_page_load_timeout(1)
        try:
            self.pub.table_BtnClick(u'提前还款申请')
        except TimeoutException as e:
            print e
        #填写退款金额相关信息
        if self.get_alert_presentname() == False :
            self.pub.goNewWindow(oldhs)
            #self.pub.goNameWindow('小牛消费金融业务管理系统')
            self.pub.comeinifm('ObjectList')
            self.pub.table_BtnClick(u'确定')
            print "00000000009999999999999999888888888888888"
            self.pub.is_alert_and_close_and_get_text()
            self.pub.winClose()
        else:
            self.pub.is_alert_and_close_and_get_text()


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def get_alert_presentname(self):
        alertname = ""
        try:
            print "1111111111111111111111111"
            alert = self.driver.switch_to_alert()
            alertname = alert.text
            print alertname
            print "00000000000000000"
            #print alert.title.strip()
            print "22222222222222222222222222"
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

