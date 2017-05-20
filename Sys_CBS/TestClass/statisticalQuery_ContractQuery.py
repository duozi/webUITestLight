# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
import unittest, time, re,threading, httplib

class StatisticalQueryContractQuery(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
    logstu = ""  # 接收main脚本传递来的写log的对象
    right_between_btn = [u'审批通过',u'审批未通过',u'导出Excel']

    #审批未通过, 未通过原因 控件
    approval_nopass_reason_sel = (By.CSS_SELECTOR,"select[id=\"R0F0\"]")
    #审批未通过, 未通过备注 控件
    approval_nopass_remarks_sel = (By.CSS_SELECTOR,"textarea[id=\"R0F1\"]")
    #页面控件元素别
    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_StatisticalQueryContractQuery(self):
        driver = self.driver
        #driver =webdriver.Firefox()

        #确认是否需要登录
        if (self.dict_data["登录用户"] <> "" and self.dict_data["登录密码"] <> ""):
            self.comm.goto_menu(driver,self.row)
        #获取操作类型
        opt = self.dict_data["操作类型"].split("|")
        #中间按扭的操作
        if opt[0] == u'申请退款':
            self.logstu.info("开始申请退款流程")
            self.apply_refund()
        if opt[0] == u'申请退保':
            self.logstu.info("开始申请退保流程")
            self.apply_return()
        if opt[0] == u'申请退货':
            self.logstu.info("开始申请退货流程")
            self.apply_goods()
        if opt[0] == u'代扣账号变更':
            self.logstu.info("开始代扣账号变更流程")
            self.acct_reset()
        if opt[0] == u'提前还款申请':
            self.logstu.info("开始提前还款申请流程")
            self.advance_apply()
        if opt[0] == u'取消提前还款申请':
            self.logstu.info("开始取消提前还款申请流程")
            self.cancel_advance_apply()

    #申请退款
    def apply_refund(self):
        self.pub.comeinifm('right')
        self.logstu.info("执行查询操作")
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        if self.pub.is_table_getRowsCount_exist(self.row,self.comm) > 0 :
            #选择第一行数据
            self.pub.table_RowClick(1)
            self.pub.comeinifm('right')
            oldhs = self.driver.window_handles

            time.sleep(2)
            try:
                self.pub.thread_btn(u'申请退款')
            except TimeoutException as e:
                print e
            #点击详情后直接跳转到新窗口
            alertname1 = self.pub.is_alert_and_close_and_get_text()
            if alertname1 == False :
                self.pub.goNewWindow(oldhs)
                #self.pub.goNameWindow('小牛消费金融业务管理系统')
                self.pub.comeinifm('ObjectList','myiframe0')
                self.pub.table_RowClick(1)
                self.pub.comeinifm('ObjectList')
                oldhs = self.driver.window_handles
                self.driver.set_page_load_timeout(1)
                try:
                    self.pub.thread_btn(u'退款申请')
                except TimeoutException as e:
                    self.logstu.debug(e)
                #填写退款金额相关信息
                alertname2 = self.pub.is_alert_and_close_and_get_text()
                if alertname2 == False :
                    self.pub.goNewWindow(oldhs)
                    #self.pub.goNameWindow('小牛消费金融业务管理系统')
                    self.pub.setEditTableValueFast(self.dict_data,'ObjectList','myiframe0')
                    self.pub.comeinifm('ObjectList')
                    self.pub.table_BtnClick(u'保存')
                    resluttext = self.pub.is_alert_and_close_and_get_text2()
                    self.logstu.info(resluttext)
                    updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                                % (self.actdb.casetitle_cn['执行结果'], resluttext, self.dict_data['test_id'])
                    self.actdb.testCaseUpdate(updatestr)
                    self.pub.winClose()
                else:
                    updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                                % (self.actdb.casetitle_cn['执行结果'], alertname2, self.dict_data['test_id'])
                    self.actdb.testCaseUpdate(updatestr)
                self.pub.winClose()
            else:
                self.logstu.debug("点击按扭申请退款后,弹出提示框是: " + alertname1)
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                            % (self.actdb.casetitle_cn['执行结果'], alertname1, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)


   #申请退保
    def apply_return(self):
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        if self.pub.is_table_getRowsCount_exist(self.row,self.comm) > 0:
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
                self.pub.setEditTableValueFast(self.dict_data,'ObjectList','myiframe0')
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
                self.pub.winClose()
            else:
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                            % (self.actdb.casetitle_cn['执行结果'], alertname1, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
            self.pub.winClose()

  #申请退货
    def apply_goods(self):
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        CFindex = ""
        if self.pub.is_table_getRowsCount_exist(self.row,self.comm) > 0 :
            #选择第一行数据
            self.pub.table_RowClick(1)
            CFindex = self.pub.table_getValue(1,"合同编号")
            self.pub.comeinifm('right')
            oldhs = self.driver.window_handles
            self.driver.set_page_load_timeout(1)
            try:
                self.pub.table_BtnClick(u'申请退货')
            except TimeoutException as e:
                print e
            #点击详情后直接跳转到新窗口
            alertname1 = self.pub.is_alert_and_close_and_get_text()
            if alertname1 == False :
                self.pub.goNewWindow(oldhs)
                #self.pub.goNameWindow('小牛消费金融业务管理系统')
                self.pub.setEditTableValueFast(self.dict_data,'ObjectList','myiframe0')
                self.pub.comeinifm('ObjectList')
                oldhs = self.driver.window_handles
                self.driver.set_page_load_timeout(1)
                try:
                    self.pub.table_BtnClick('上传电子扫描件')
                except TimeoutException as e:
                    print e
                self.pub.goNewWindow(oldhs)
                self.pub.comeinifm('ObjectList')
                upload_rult = self.pub.all_type_to_encode(self.pub.uploadfile('2.jpg'))
                self.assertNotEqual(upload_rult.find('上传文件成功'), -1)
                self.driver.switch_to_default_content()
                self.pub.winClose() # 关闭上传文件弹窗
                self.pub.comeinifm('ObjectList')
                self.pub.table_BtnClick(u'保存')
                resluttext = self.pub.is_alert_and_close_and_get_text2()
                self.logstu.info(resluttext)
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                            % (self.actdb.casetitle_cn['执行结果'], resluttext, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                self.pub.winClose()
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                            % (self.actdb.casetitle_cn['主键备注'], CFindex, self.dict_data['test_id'])
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
        if self.pub.is_table_getRowsCount_exist(self.row,self.comm):
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
            alertname1 = self.pub.is_alert_and_close_and_get_text()
            if alertname1 == False :
                self.pub.goNewWindow(oldhs)
                #self.pub.goNameWindow('小牛消费金融业务管理系统')
                self.pub.setEditTableValueFast(self.dict_data,'ObjectList','myiframe0')
                self.pub.comeinifm('ObjectList')
                oldhs = self.driver.window_handles
                self.driver.set_page_load_timeout(1)
                try:
                    self.pub.table_BtnClick(u'确认变更')
                except TimeoutException as e:
                    print e
                time.sleep(0.5)
                self.pub.close_alert_and_get_its_text()
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
                self.comm.write_reslut(resluttext,self.row)
                self.pub.winClose()
                self.pub.winClose()
            else:
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                            % (self.actdb.casetitle_cn['执行结果'], alertname1, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)


    #提前还款申请
    def advance_apply(self):
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right','myiframe0')
        if self.pub.is_table_getRowsCount_exist(self.row,self.comm) > 0:
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
            alertname1 = self.pub.is_alert_and_close_and_get_text()
            if alertname1 == False :
                self.pub.goNewWindow(oldhs)
                #self.pub.goNameWindow('小牛消费金融业务管理系统')
                self.pub.comeinifm('ObjectList')
                self.pub.table_BtnClick(u'确定')
                resluttext = self.pub.is_alert_and_close_and_get_text2()
                self.logstu.info(resluttext)
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                            % (self.actdb.casetitle_cn['执行结果'], resluttext, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                self.pub.winClose()
            else:
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                            % (self.actdb.casetitle_cn['执行结果'], alertname1, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)

    #取消提前还款申请
    def cancel_advance_apply(self):
        self.pub.comeinifm('right')
        oldhs = self.driver.window_handles
        #self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(1)
        try:
            self.pub.table_BtnClick(u'取消提前还款申请')
        except TimeoutException as e:
            print e
        #self.thread_main(u'取消提前还款申请')
        time.sleep(5)
        try:
            self.pub.goNewWindow(oldhs)
        except httplib.CannotSendRequest as e:
            print e
        #self.pub.goNameWindow('小牛消费金融业务管理系统')
        self.pub.comeinifm('ObjectList')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('ObjectList','myiframe0')
        if self.pub.is_table_getRowsCount_exist(self.row,self.comm) > 0:
            #选择第一行数据
            self.pub.table_RowClick(1)
            self.pub.comeinifm('ObjectList')
            self.pub.table_BtnClick(u'取消提前还款')
            self.pub.is_alert_and_close_and_get_text()
            resluttext = self.pub.is_alert_and_close_and_get_text2()
            self.logstu.info(resluttext)
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'], resluttext, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.winClose()

    def thread_btn(self,btnname):
        try:
            self.pub.table_BtnClick(btnname)
        except TimeoutException as e:
            print e

    def thread_main(self,btnname):
        threads = []
        t1 = threading.Thread(target=self.thread_btn,args=(btnname,))
        t1.setDaemon(True)
        t1.start()

    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

