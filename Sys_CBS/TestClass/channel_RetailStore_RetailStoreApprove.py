#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import time,os
from Sys_CBS.PageObj.commFunction import CommFunction
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException, NoSuchWindowException
from selenium.webdriver.common.by import By

class ChannelRetailStoreRetailStoreApprove(unittest.TestCase):
    '''渠道管理  商户门店管理  商户门店准入审批'''
    # 产品管理-商品类型：增删改查
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数（测试数据列表的index数）
    actdb = None  # 接收main脚本传送的mysql处理类对象
    logstu = ""  # 接收main脚本传递来的写log的对象


    textarea_issueOpini = (By.CSS_SELECTOR, 'textarea#R0F2') # 审核中-签署意见输入框
    select_commit = (By.ID, 'PhaseOpinion1')  # 审核中-意见选择列表
    btn_commit = (By.ID, 'buttonmiddletd21')  # 提交按钮

    def write_textarea_issueOpini(self, value):
        textarea_io = self.driver.find_element(*self.textarea_issueOpini)
        textarea_io.clear()
        textarea_io.send_keys(value)

    def setUp(self):
        self.driver = self.mainWebDr
        # self.comm = CommFunction()
        self.pub = PublicAct(self.driver)
        self.logstu.info(self.pub.all_type_to_encode(self.dict_data["案例名称"]) + '---' + self.pub.all_type_to_encode(
            self.dict_data["案例详情"]))
        # 进入具体菜单项
        self.pub.comeinifm()
        #self.comm.goto_menu(self.driver, self.row)
        self.pub.goto_menu(self.dict_data)
        self.pub.leftMenuVagueClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[0], 'left')

    # 测试流程
    def test_RetailStoreApply(self):
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '审核':
            self.logstu.debug(u'审核')
            self.waitAudit()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '签署意见':
            self.logstu.debug(u'签署意见')
            self.issueOpini()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '提交':
            self.logstu.debug(u'提交')
            self.commit_Auditing()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '确认协议':
            self.logstu.debug(u'确认协议')
            self.confirm_agreement()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '已完成':
            self.logstu.debug(u'已完成')
            self.select_result()
    # 查询操
    def selectStore(self):
        driver = self.driver
        self.pub.comeinifm('right')
        # self.pub.select_sets(self.dict_data)
        # self.pub.select_btn(u'查询')
        self.pub.selectAutoSets(self.dict_data)
        driver.switch_to_default_content()

    # 商户门店准入审批-待审核-审核
    def waitAudit(self):
        driver = self.driver
        self.selectStore()
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        #self.pub.table_RowClick(1)
        self.pub.table_RowCheckBox(1)

        self.pub.comeinifm('right')
        self.pub.base_thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])

        self.logstu.debug(u'商户门店准入审批-待审核-审核：')
        okrl = self.pub.all_type_to_encode(self.dict_data["预期结果"])
        try:
            auditrl = self.pub.all_type_to_encode(self.pub.is_alert_and_close_and_get_text2())
        except NoAlertPresentException as e:
            self.logstu.debug(e)
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
            % (self.actdb.casetitle_cn['执行结果'], auditrl, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        self.assertNotEqual(auditrl.find(okrl), -1, '审核预期结果：' + okrl + '  | 实际执行结果：' + auditrl)

    # 商户门店准入审批-审核中-签署意见
    def  issueOpini(self):
        driver = self.driver
        self.selectStore()
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)

        self.pub.comeinifm('right')

        oldhs = driver.window_handles
        driver.set_page_load_timeout(1)
        try:
            self.pub.thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])
        except TimeoutException as e:
            self.logstu.debug(e)
        self.pub.goNewWindow(oldhs)

        self.pub.comeinifm('ObjectList', 'myiframe0')
        self.write_textarea_issueOpini(self.dict_data["输入值1"].split('|')[1])
        self.pub.comeinifm('ObjectList')
        self.pub.thread_btn(u'确认')
        driver.switch_to_default_content()
        self.pub.winClose()

    # 商户门店准入审批-审核中-提交
    def commit_Auditing(self):
        driver = self.driver
        self.selectStore()
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)

        self.pub.comeinifm('right')

        oldhs = driver.window_handles
        driver.set_page_load_timeout(1)
        try:
            self.pub.thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])
        except TimeoutException as e:
            self.logstu.debug(e)
        self.pub.goNewWindow(oldhs)

        phaseOpinion = driver.find_element(*self.select_commit)
        allOptions = phaseOpinion.find_elements_by_tag_name("option")
        driver.set_page_load_timeout(15)
        for v in allOptions:
            if self.pub.all_type_to_encode(v.text) == self.pub.all_type_to_encode(self.dict_data["输入值1"].split('|')[1]):
                v.click()
                break
        driver.find_element(*self.btn_commit).click()
        commit_txt = self.pub.close_alert_and_get_its_text()
        self.logstu.debug(commit_txt)   # 该笔业务的下一阶段: 后台管理专员审核; 你确定提交吗？

        commitrl = ''
        okrl = self.pub.all_type_to_encode(self.dict_data["预期结果"])
        if self.pub.all_type_to_encode(commit_txt).find(okrl) == -1:
            for i in range(0, 10):
                if self.pub.is_alert_present(self.driver):
                    try:
                        commitrl = self.pub.all_type_to_encode(self.pub.close_alert_and_get_its_text())
                        if str(commitrl) == 'False':
                            continue
                        if str(commitrl).find(okrl) != -1:
                            break
                    except NoAlertPresentException as e:
                        self.logstu.debug(e)
                    except NoSuchWindowException as e:
                        self.logstu.debug(e)
                        driver.switch_to_window(oldhs[0])
                time.sleep(0.5)
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'], commitrl, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.assertNotEqual(commitrl.find(okrl), -1, '审核预期结果：' + okrl + '  | 实际执行结果：' + commitrl)


    # 待审核（提交）->审核中（提交）->待协议确认（确认协议）
    def confirm_agreement(self):
        driver = self.driver
        self.selectStore()
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)
        self.pub.comeinifm('right')
        self.pub.base_thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])

        commit_txt = self.pub.close_alert_and_get_its_text()
        self.logstu.debug(commit_txt) # 您真的想将该条信息确认协议吗？

        commitrl = ''
        okrl = self.pub.all_type_to_encode(self.dict_data["预期结果"])
        for i in range(0,6):
            try:
                commitrl = self.pub.all_type_to_encode(self.pub.is_alert_and_close_and_get_text2())
                self.logstu.debug('门店申请待确认协议，提交后第2个alert：')
                self.logstu.debug(commitrl)
                if commitrl.find(okrl) != -1:
                    break
            except NoAlertPresentException as e:
                self.logstu.debug(e)
            time.sleep(1)
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], commitrl, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        self.assertNotEqual(commitrl.find(okrl), -1, '审核预期结果：' + okrl + '  | 实际执行结果：' + commitrl)


    # 已完成-通过-通过的任务
    def select_result(self):
        driver = self.driver
        self.selectStore()
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        count = self.pub.table_getRowsCount()
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], "查询到数据个数：" + str(count), self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        self.assertEqual(count,int(self.dict_data["预期结果"]))



