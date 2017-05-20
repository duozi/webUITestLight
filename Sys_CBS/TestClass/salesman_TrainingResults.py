#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest,time,os
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException, NoSuchWindowException


class SalesmanTrainingResults(unittest.TestCase):
    '''培训结果登记'''
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
    logstu = "" # 接收main脚本传递来的写log的对象

    def setUp(self):
        self.driver = self.mainWebDr
        # self.comm = CommFunction()
        self.pub = PublicAct(self.driver)

        # 进入具体菜单项
        self.logstu.info(self.pub.all_type_to_encode(self.dict_data["案例名称"]) + '---' + self.pub.all_type_to_encode(
            self.dict_data["案例详情"]))
        self.pub.comeinifm()
        #self.comm.goto_menu(self.driver, self.row)
        self.pub.goto_menu(self.dict_data)
        self.pub.leftMenuClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[0], 'left')
        #self.pub.leftMenuVagueClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[0], 'left')



    # 测试类
    def test_SalesmanTrainingResults(self):
        driver = self.driver
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '详情查看':
            self.logstu.info(u'详情查看')
            self.recordScores()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '通过':
            self.logstu.info(u'通过')
            self.passAct()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '考试结果上传':
            self.logstu.info(u'考试结果上传')
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '获取用户编号':
            self.logstu.info(u'获取用户编号')
            self.get_userno()

    #获取用户的编号，add by limeng
    def get_userno(self):
        cert_id = self.dict_data['查询条件1'].split('|')[1]
        #cert_id = '450923199605167216'
        driver = self.driver
        #点击账号管理
        self.pub.comeinifm('left')
        self.pub.click_btn(driver.find_element_by_id('text2'))
        time.sleep(3)
        #输入省份证号，查询出用户的编号
        self.pub.comeinifm('right')
        cert_id = self.pub.all_type_to_unicode(cert_id)
        self.pub.input_text(driver.find_element_by_id('DF3_1_INPUT'),cert_id)
        time.sleep(3)
        self.pub.select_btn(u'查询')
        self.pub.comeinifm('right','myiframe0')
        time.sleep(3)
        element = driver.find_element_by_name('R0F0')
        #身份证号写入表中
        value = element.get_attribute("value")
        time.sleep(2)
        updatesql = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'], value, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatesql)
        #self.comm.write_file(value,self.row,self.comm.get_key_cell_col("执行结果"))

    # 详情查看页面 录入分数
    def recordScores(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)
        self.pub.comeinifm('right')

        oldhs = driver.window_handles
        driver.set_page_load_timeout(1)
        try:
            self.pub.thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])
        except TimeoutException as e:
            self.logstu.debug(e)
        driver.set_page_load_timeout(30)
        self.pub.goNewWindow(oldhs)

        self.pub.comeinifm('ObjectList', 'myiframe0')
        #self.pub.setEditTableValues(self.dict_data, 'ObjectList', 'myiframe0')
        self.pub.setEditTableValueFast(self.dict_data, 'ObjectList', 'myiframe0')
        self.pub.comeinifm('ObjectList')
        self.pub.thread_btn('保存')
        self.pub.comeinifm()
        self.pub.winClose()

    # 通过操作
    def passAct(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowCheckBox(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])
        commitrl = ''
        if self.pub.is_alert_present(self.driver):
            try:
                commitrl = self.pub.all_type_to_encode(self.pub.close_alert_and_get_its_text())
            except NoAlertPresentException as e:
                self.logstu.debug(e)
        okrl = self.pub.all_type_to_encode(self.dict_data["预期结果"])
        self.logstu.debug(u'执行结果【' + self.pub.all_type_to_unicode(commitrl)
                          + u'】写入testcals.xls，\r\n预期结果为：' + self.pub.all_type_to_unicode(okrl))
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], commitrl, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        self.assertNotEqual(commitrl.find(okrl), -1, '审核预期结果：' + okrl + '  | 实际执行结果：' + commitrl)

