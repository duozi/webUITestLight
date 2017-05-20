# -*- coding: utf-8 -*-
import time

from Sys_CBS.PageObj.commFunction import CommFunction
from Sys_CBS.PageObj.getElements import LoginElement
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException


class SalesmanFunction():
    def __init__(self, driver):
        self.driver = driver
        #self.dict_data = test_dict_data  # 接收excel用例参数
        self.comm = CommFunction()
        self.pub = PublicAct(self.driver)

    ### 销售入职管理模块调用的公共方法
    #选中第一行数据
    def table_RowClick1(self,rownum):
        driver = self.driver
        rnum = self.pub.table_getRowsCount()
        rnum1 = self.table_getRowsCount()
        #cnum = self.pub.table_getColumnsCount()
        print "行数：",rnum
        print "行数11111111111：",rnum1

        #print "列数：",cnum
        print driver.find_elements(*self.pub.table_tr)[rownum + 1]
        driver.find_elements(*self.pub.table_tr)[rownum + 1].find_elements_by_tag_name('td')[2].click()


    # 勾选审核列表表格中的数据
    def table_RowClick(self, rownum):
        driver = self.driver
        #tabclass = PubTableItemElement()
        #driver.find_elements(*self.table_tr)[rownum + 1].click()
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        print "行数：",rnum
        print "列数：",cnum
        driver.find_elements(*self.pub.table_tr)[rownum + 1].find_elements_by_tag_name('td')[1].click()

        #传参数：查询数据，按钮
        #num 查询条件，身份证号
        #获取任务，输入查询条件查询，选中第一行数据
    def GetData(self,value):
        driver = self.driver
        value = self.all_type_to_unicode(value)
        self.pub.comeinifm("right")
        self.pub.thread_btn(u'批量获取任务')
        time.sleep(1)
        try:driver.switch_to_alert().accept()
        except NoAlertPresentException as e:print e
        time.sleep(1)
        try:driver.switch_to_alert().accept()
        except NoAlertPresentException as e:print e
        driver.implicitly_wait(6)
        driver.find_element_by_id('DF4_1_INPUT').send_keys(value)
        self.pub.select_btn(u'查询')
        print "1111111111111111111111111111111111111111111"
        driver.switch_to_default_content()
        self.pub.comeinifm('right','myiframe0')
        self.table_RowClick1(-2)


    #针对点击后会弹出窗口的按钮
    #点击按钮，
    def BtnClick(self,btnname):
        driver = self.driver
        btnname = self.all_type_to_unicode(btnname)
        self.pub.comeinifm('right')
        for i in range(0,5):
            if len(driver.window_handles) == 1:
                print "第",i,"次查询",driver.window_handles
                driver.set_page_load_timeout(10)
                try:self.pub.thread_btn(btnname)
                except TimeoutException as e:print e
                driver.set_page_load_timeout(30)


       # 获取表格数据行数,########电话审核弹出框的列表表格
    def table_getRowsCount(self):
        driver = self.driver
        #tabclass = PubTableItemElement()
        #driver = webdriver.Firefox()
        table_tr = driver.find_elements(*self.pub.table_tr)
        return len(table_tr)

    #反欺诈初审，电话核查,###先获取行数，再对每行的下拉框选中“是”
    #Number 参数为列表行数
    def SetValue(self,Number):
        driver = self.driver
        self.pub.comeinifm('ObjectList','myiframe0')
        for ii in range(0,Number):
            print ii
            select = driver.find_elements(*self.pub.table_tr)[ii].find_elements_by_tag_name('select')
            print len(select)
            if len(select) > 1:
                ops = driver.find_elements(*self.pub.table_tr)[ii].find_elements_by_tag_name('option')
                print len(ops)
                time.sleep(2)
                for op1 in ops:
                    if op1.tag_name == 'option' and op1.get_attribute('value') == '1':
                        op1.click()
        driver.switch_to_default_content()

    #保存后关闭弹出，切换到旧窗口
    #oldhandle   调用之前需要获取旧窗口句柄
    def ReturnOldWin(self,oldhandle):
        driver = self.driver
        self.pub.comeinifm('ObjectList')
        self.pub.thread_btn(u'保存')
        driver.switch_to_default_content()
        driver.implicitly_wait(10)
        self.pub.winClose()
        driver.switch_to_window(oldhandle)

    #提交
    def getAlertText(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.logstu.error('6666666666666666666666666666666')
        self.pub.logstu.error(self.pub.thread_btn(u'提交'))

        Result2 =driver.switch_to_alert().text.strip(u"！").find(u'提交成功')
        self.pub.logstu.error('77777777777777777777777')
        self.pub.logstu.error(Result2)
        if  Result2 == 0:
            self.pub.logstu.error('Result2 == 0')
            return self.pub.is_alert_and_close_and_get_text()
            '''
            try:driver.switch_to_alert().accept()
            except NoAlertPresentException as e:self.pub.logstu.debug(e)
            return Result2'''
        elif Result2 == -1:
            self.pub.logstu.error('Result2 == -1')
            #return self.pub.is_alert_and_close_and_get_text()

            try:driver.switch_to_alert().accept()
            except NoAlertPresentException as e:print e
            driver.implicitly_wait(5)
            Alert1 = driver.switch_to_alert()
            Result3 = Alert1.text.strip(u"！").find(u'提交成功')
            try:
                self.pub.logstu.debug(u'Alert1.text:\n\t' + Alert1.text)
                Alert1.accept()
            except NoAlertPresentException as e:print e
            return Result3















    def is_alert_present(self,drive_in):
        try: drive_in.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def all_type_to_unicode(self,str_in):
        #处理字符编码问题
        if isinstance(str_in, float):
            str_in = int(str_in)
        elif isinstance(str_in, unicode):
            pass
        else:
            str_in = unicode(str_in,"utf-8")
        return str_in

    def login_success(self,login_url_in,username_in,passwd_in):
        #处理字符编码问题

        username_in = self.all_type_to_unicode(username_in)
        passwd_in = self.all_type_to_unicode(passwd_in)
        #启动浏览器
        #driver = self.get_browserdrvie('Firefox')
        driver = webdriver.Ie()
        driver.get(login_url_in)
        time.sleep(1)
        driver.find_element(*LoginElement.userEdit).clear()
        driver.find_element(*LoginElement.userEdit).send_keys(username_in)
        #输入密码
        driver.find_element(*LoginElement.passwdEdit).send_keys(passwd_in)
        #点击提交按扭
        driver.find_element(*LoginElement.submitButton).click()
        #将webdrive传回给主调用函数
        self.mainwebdrive = driver
        if self.is_alert_present(driver):
            try:driver.switch_to_alert().accept()
            except NoAlertPresentException as e: print 'NoAlertPresentException: login switch_to_alert'
        return driver
