# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException,StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from Sys_CBS.PageObj.salesmanFunction import SalesmanFunction
from Sys_CBS.PageObj.jFunction import Function
import unittest, time, re

class SalesmanCheckApply(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row =""          #接收main脚本传送的当前处理的行数
    ##列表中'审批结果'字段
    approve_result= (By.CSS_SELECTOR, "select[name=\"R0F48\"]")
    ##列表中'拒绝原因'字段
    reject_reason = (By.CSS_SELECTOR, "select[name=\"R0F49\"]")
    ########## 安全部调查  -> 背景调查 弹窗中的‘调查结果’字段
    survey_result = (By.ID, 'R0F4')


    def setUp(self):
        #self.driver = self.comm.get_browserdrvie('Chrome')
        self.driver = self.mainWebDr
        self.driver.implicitly_wait(30)
        self.pub = PublicAct(self.driver)
        self.salesman = SalesmanFunction(self.driver)

        self.verificationErrors = []
        self.accept_next_alert = True
        self.execldata = ""
        self.filepath = ""
        # 进入具体菜单
        # self.comm.goto_menu(self.driver,self.row)
        self.pub.goto_menu(self.dict_data)



    def test_SalesmanCheckApply(self):

        if self.dict_data["操作类型"].encode('utf8') == '反欺诈初审':
            self.pub.logstu.info(u'反欺诈审核流程')
            self.pub.logstu.debug(u'用例序号：'+str(self.row))
            self.first_approve()
        if self.dict_data["操作类型"].encode('utf8') == '安全调查':
            self.pub.logstu.info(u'安全调查流程')
            self.pub.logstu.debug(u'用例序号：' + str(self.row))
            self.security_survey()
        if self.dict_data["操作类型"].encode('utf8') == '反欺诈终审':
            self.pub.logstu.info(u'反欺诈终审流程')
            self.pub.logstu.debug(u'用例序号：' + str(self.row))
            self.last_approver()
        if self.dict_data["操作类型"].encode('utf8') == '反欺诈终审背景调查失败':
            self.pub.logstu.info(u'反欺诈终审拒绝--背景调查失败和风控原因')
            self.pub.logstu.debug(u'用例序号：' + str(self.row))
            self.last_approver_reason_background_check_fail()
        if self.dict_data["操作类型"].encode('utf8') == '反欺诈终审非背景调查失败':
            self.pub.logstu.info(u'反欺诈终审拒绝--除背景调查失败和风控的其他12项原因')
            self.pub.logstu.debug(u'用例序号：' + str(self.row))
            self.last_approver_reason_Notbackground_check_fail()
        if self.dict_data["操作类型"].encode('utf8') == '反欺诈终审失败':
            reason = self.dict_data['输入值1'].split('|')[1]
            self.pub.logstu.info(u'反欺诈终审拒绝--原因为：%s' % reason)
            self.pub.logstu.debug(u'用例序号：' + str(self.row))
            self.last_approver_fail()

    #add by liemng
    def last_approver_fail(self):
        driver = self.driver
        #获取身份证号码和失败原因
        cert_id = self.dict_data['查询条件1'].split('|')[1]
        #cert_id = "120102198506020001"
        reason  = self.dict_data['输入值1'].split('|')[1]
        self.pub.leftMenuVagueClick(u'待处理申请>反欺诈终审','left')
        self.get_alltask()
        #刷新当前页面
        time.sleep(2)
        # 查询出对应的销售人员
        self.pub.input_text(driver.find_element_by_css_selector("input[name='DOFILTER_DF4_1_VALUE'][id='DF4_1_INPUT']"),cert_id)
        self.pub.select_btn(u'查询')
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.click_btn(driver.find_element_by_name("R0F0"))
        s = driver.find_element_by_css_selector("select[name='R0F48'][class='GdTdContentSelect']")
        s.find_element_by_xpath("//option[@value='拒绝']").click()
        time.sleep(1)
        s1 = driver.find_element_by_css_selector("select[name='R0F49'][class='GdTdContentSelect']")
        list = s1.find_elements_by_xpath("//option[@value]" )# 选择拒绝的原因
        #选择拒绝原因
        for opt in list:
            if opt.text == reason:
                self.logstu.info(u"选择拒绝原因：%s" % reason)
                opt.click()
        #提交
        self.pub.comeinifm('right')
        self.pub.table_BtnClick_NoSetTimeOut("提交")
        self.pub.is_alert_and_close_and_get_text()
        time.sleep(4)


    def first_approve(self):

        driver = self.driver
        #点击左侧 ‘反欺诈审核’菜单
        self.pub.leftMenuVagueClick(u'待处理申请>反欺诈审核','left')
        # 调用函数，批量获取任务并查询
        self.get_alltask()
        self.pub.selectAutoSet(u'身份证号', u'等于', self.dict_data['查询条件1'].split('|')[1])
        self.pub.logstu.debug(u'查询条件：' + self.dict_data['查询条件1'].split('|')[1])
        self.pub.logstu.debug('11111111111111111111111111111111111111')
        time.sleep(2)
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()
        ######## 选中第一行数据
        self.pub.comeinifm('right', 'myiframe0')
        self.salesman.table_RowClick1(-2)
        ###### 填写审核结果
        self.approveresult_set()
        driver.switch_to_default_content()
        #### 执行电话审核
        if self.dict_data['输入值3'][1] == u'是':
            self.telephone_approve()
        else:self.pub.logstu.debug(u'不执行电话审核')
        #调用函数，勾选第一行数据
        self.pub.comeinifm('right','myiframe0')
        self.salesman.table_RowClick(-2)
        time.sleep(3)
        driver.switch_to_default_content()
        #点击提交按钮，并且判断是否提交成功
        #判断用例是否执行成功
        #self.assertNotEqual(self.salesman.getAlertText(),-1)
        rul = self.getAlertText()
        self.pub.logstu.debug(rul)
        self.pub.logstu.cri(u'test end...............................')

    def security_survey(self):

        driver = self.driver
        #点击左侧 ‘安全部调查’菜单
        self.pub.leftMenuVagueClick(u'待处理申请>安全部调查','left')
        # 调用函数，批量获取任务并查询
        self.get_alltask()
        self.pub.selectAutoSet(u'身份证号', u'等于', self.dict_data['查询条件1'].split('|')[1])
        self.pub.logstu.debug(u'查询条件：' + self.dict_data['查询条件1'].split('|')[1])
        self.pub.logstu.debug('11111111111111111111111111111111111111')
        time.sleep(2)
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()
        ######## 选中第一行数据
        self.pub.comeinifm('right', 'myiframe0')
        self.salesman.table_RowClick1(-2)
        ###### 填写审核结果
        self.approveresult_set()
        driver.switch_to_default_content()
        ####  执行背景调查
        self.background_check(self.dict_data['输入值3'].split('|')[1])
        # 调用函数，勾选第一行数据
        self.pub.comeinifm('right','myiframe0')
        self.salesman.table_RowClick(-2)
        time.sleep(3)
        driver.switch_to_default_content()
        #点击提交按钮，并且判断是否提交成功
        #判断用例是否执行成功
        self.assertNotEqual(self.getAlertText(),-1)

    def last_approver(self):

        driver = self.driver
        #点击左侧 ‘反欺诈终审’菜单
        self.pub.leftMenuVagueClick(u'待处理申请>反欺诈终审','left')
        #调用函数，批量获取任务并查询
        self.get_alltask()
        self.pub.selectAutoSet(u'身份证号', u'等于', self.dict_data['查询条件1'].split('|')[1])
        self.pub.logstu.debug(u'查询条件：' + self.dict_data['查询条件1'].split('|')[1])
        self.pub.logstu.debug('11111111111111111111111111111111111111')
        time.sleep(2)
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()
        #调用函数，选中第一行数据
        self.pub.comeinifm('right','myiframe0')
        self.salesman.table_RowClick(-2)

        ###### 填写审核结果
        self.approveresult_set()
        driver.switch_to_default_content()
        #点击提交按钮，并且判断是否提交成功
        #判断用例是否执行成功
        self.assertNotEqual(self.getAlertText(),-1)

    def last_approver_reason_background_check_fail(self):
        driver = self.driver
        # 点击左侧 ‘反欺诈终审’菜单
        self.pub.leftMenuVagueClick(u'待处理申请>反欺诈终审', 'left')
        # 调用函数，获取任务并查询
        self.get_alltask()
        driver.switch_to_default_content()
        #####刷新当前页面
        driver.execute_script('location.reload(true)')
        self.pub.logstu.debug(u'JS执行成功')
        self.pub.comeinifm('right', 'myiframe0')
        #######批量填写拒绝原因
        self.reject_reasons_set(2)
        driver.switch_to_default_content()
        # 点击提交按钮，并且判断是否提交成功
        # 判断用例是否执行成功
        self.assertNotEqual(self.getAlertText(), -1)

    def last_approver_reason_Notbackground_check_fail(self):
        driver = self.driver
        # 点击左侧 ‘反欺诈终审’菜单
        self.pub.leftMenuVagueClick(u'待处理申请>反欺诈终审', 'left')
        # 调用函数，获取任务并查询
        self.get_alltask()
        driver.switch_to_default_content()
        #####刷新当前页面
        driver.execute_script('location.reload(true)')
        self.pub.comeinifm('right', 'myiframe0')
        #######批量填写拒绝原因

        self.reject_reasons_set(12)
        driver.switch_to_default_content()
        # 点击提交按钮，并且判断是否提交成功
        # 判断用例是否执行成功
        self.assertNotEqual(self.getAlertText(), -1)



    def getAlertText(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.logstu.error('6666666666666666666666666666666')
        self.pub.logstu.error(self.pub.thread_btn(u'提交'))
        Result2 = driver.switch_to_alert().text.strip(u"！").find(u'提交成功')
        self.pub.logstu.error('77777777777777777777777')
        self.pub.logstu.error(Result2)
        if Result2 == 0:
            self.pub.logstu.error('Result2 == 0')
            return self.pub.is_alert_and_close_and_get_text()
            '''
            try:driver.switch_to_alert().accept()
            except NoAlertPresentException as e:self.pub.logstu.debug(e)
            return Result2'''
        elif Result2 == -1:
            self.pub.logstu.error('Result2 == -1')
            # return self.pub.is_alert_and_close_and_get_text()
            try:
                alert11 = driver.switch_to_alert()
                self.pub.logstu.cri(alert11.text)
                alert11.accept()
            except NoAlertPresentException as e:
                self.pub.logstu.debug(e)
            self.pub.logstu.debug(u'开始操作第二个alert window')
            Alert1 = driver.switch_to_alert()
            #self.pub.logstu.cri(Alert1.text)
            Result3 = Alert1.text.strip(u"！").find(u'提交成功')
            try:
                self.pub.logstu.debug(u'Alert1.text:\n\t' + Alert1.text)
                Alert1.accept()
            except NoAlertPresentException as e:
                self.pub.logstu.debug(e)
            return Result3

    def get_alltask(self):
        driver = self.driver
        self.pub.comeinifm("right")
        self.pub.thread_btn(u'批量获取任务')
        try:
            alert1 = driver.switch_to_alert()
            self.pub.logstu.debug(u'第一个弹框的文本信息：' + alert1.text)
            alert1.accept()
        except NoAlertPresentException as e:
            self.pub.logstu.error(e)
        time.sleep(2)
        if driver.switch_to_alert():
            self.pub.logstu.debug(u'开始操作第二个弹框')
            try:
                alert2 = driver.switch_to_alert()
                self.pub.logstu.debug(u'第二个弹框的文本信息：' + alert2.text)
                alert2.accept()
            except NoAlertPresentException as e:
                self.pub.logstu.error(e)
        #driver.switch_to_default_content()

    def get_task(self):
        driver = self.driver
        #self.pub.select_set('4','4',self.dict_data['查询条件1'].split('|')[1])
        self.pub.selectAutoSet(u'身份证号',u'等于',self.dict_data['查询条件1'].split('|')[1])
        self.pub.logstu.debug(u'查询条件：'+self.dict_data['查询条件1'].split('|')[1])
        self.pub.logstu.debug('11111111111111111111111111111111111111')
        time.sleep(2)
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()

    ###### 审核结果填写
    def approveresult_set(self):
        driver = self.driver
        ApproveResult = self.dict_data['输入值1'].split('|')[1]
        RejectReason = self.dict_data['输入值2'].split('|')[1]
        options = driver.find_element(*self.approve_result).find_elements_by_tag_name('option')
        options2 = driver.find_element(*self.reject_reason).find_elements_by_tag_name('option')
        for option in options:
            if ApproveResult == option.get_attribute('value') == u'同意':
                option.click()
                break
            if ApproveResult == option.get_attribute('value') == u'拒绝':
                option.click()
                for option2 in options2:
                    if RejectReason == option2.text:
                        self.pub.logstu.debug(option2.text)
                        option2.click()
                        break
    ### 执行电话审核
    def telephone_approve(self):
        driver = self.driver
        current_handle = driver.current_window_handle  # 获取当前窗口句柄
        self.pub.logstu.debug("旧的句柄:")
        self.pub.logstu.debug(current_handle)  # 输出当前获取的窗口句柄
        self.salesman.BtnClick(u'电话核查')
        self.pub.goNameWindow(u'小牛消费金融业务管理系统')
        # 调用函数，执行电话审核
        self.pub.comeinifm("ObjectList", "myiframe0")
        rownumber = self.salesman.table_getRowsCount()
        # rownumber = self.salesman.table_getRowsCount()
        self.pub.logstu.debug("电话审核列表行数：" + str(rownumber))
        self.salesman.SetValue(rownumber)
        # 保存，关闭弹框并切换到旧窗口
        self.pub.comeinifm("ObjectList")
        self.pub.thread_btn(u'保存')
        time.sleep(3)
        self.pub.logstu.debug('sleep 3 close window start')
        self.pub.winClose2()
        time.sleep(3)
    ######## 执行背景调查，
    ##### 参数为需要填写的背景调查字段
    def background_check(self,surveyresult):
        driver = self.driver
        surveyresult = self.pub.all_type_to_unicode(surveyresult)
        current_handle = driver.current_window_handle  # 获取当前窗口句柄
        self.salesman.BtnClick(u'背景调查')
        self.pub.goNameWindow(u'小牛消费金融业务管理系统')
        self.pub.comeinifm('ObjectList', 'myiframe0')
        # 输入调查结果
        driver.find_element(*self.survey_result).send_keys(surveyresult)
        driver.switch_to_default_content()
        # 保存，关闭弹框并切换到旧窗口
        self.pub.comeinifm("ObjectList")
        self.pub.thread_btn(u'保存')
        time.sleep(2)
        self.pub.winClose2()
    #######批量填写拒绝原因
    ###### 参数 number 为数据个数
    def reject_reasons_set(self,number):
        driver = self.driver
        rownum = self.pub.table_getRowsCount()
        self.pub.logstu.debug(rownum)
        number1 = number +1
        for count in range(1, number1):
            resultcont = '输入值' + str(count)
            RejectReason1 = self.dict_data[resultcont].split('|')[1]

            for i in range(0,10):
                self.pub.logstu.debug(u'重复次数：'+str(i))
                try:
                    trs = driver.find_elements(*self.pub.table_tr)
                    tds = trs[count + 1].find_elements_by_tag_name('td')
                    self.pub.logstu.debug(u'序列号：' + tds[0].text)
                    self.pub.logstu.debug(u'cont:' + str(count))
                    driver.implicitly_wait(10)
                    tds[1].click()
                    self.pub.logstu.debug(u'tdstdstdstdstdstdstdstdstds')
                    break
                except TimeoutException as e:
                    self.pub.logstu.error(e)
                    self.pub.logstu.debug(u'tdstds222222222222222222222222')
            ###### 填写审核结果
            # driver.find_element(*self.approve_result).find_element_by_tag_name('option')
            options = tds[4].find_elements_by_tag_name('option')
            options2 = tds[5].find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('value') == u'拒绝':
                    for i in range(0,6):
                        try:
                            option.click()
                            break
                        except TimeoutException as e:
                            self.pub.logstu.error(e)
                    for option2 in options2:
                        if RejectReason1 == option2.text:
                            self.pub.logstu.debug(option2.text)
                            option2.click()
                            break