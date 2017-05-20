#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import time,os
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException, NoSuchWindowException
from selenium.webdriver.common.by import By

class SystemUser(unittest.TestCase):
    '''系统管理>用户管理'''
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象
    actdb = None  # 接收main脚本传送的mysql处理类对象

    qx_trs_by = (By.CSS_SELECTOR, 'tr >td >div >table >tbody >tr.RoleLeafUncheck')
    savebtn_by = (By.CSS_SELECTOR, 'td#buttonmiddletd21')

    def set_QuanXian(self, qxname):
        driver = self.driver
        qx_trs = driver.find_elements(*self.qx_trs_by)
        for tr in qx_trs:
            tds = tr.find_elements_by_tag_name('td')
            if self.pub.all_type_to_encode(tds[2].text) == self.pub.all_type_to_encode(qxname):
                checkbox = tds[0].find_element_by_css_selector('input[type="checkbox"]')
                if checkbox.is_selected() == False:
                    checkbox.click()
                    return True
                else:
                    self.logstu.info(u'已有权限：' + self.pub.all_type_to_unicode(qxname))
                    return True
        return False

    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.logstu.info(self.pub.all_type_to_encode(self.dict_data["案例名称"]) + '---' + self.pub.all_type_to_encode(
            self.dict_data["案例详情"]))
        # 进入具体菜单项
        self.pub.comeinifm()
        #self.comm.goto_menu(self.driver, self.row)
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] != '首次登录':
            self.pub.goto_menu(self.dict_data)
        #self.pub.leftMenuClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[0], 'left')
        # self.pub.leftMenuVagueClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[0], 'left')

    # 测试类
    def test_SalesmanTrainingResults(self):
        driver = self.driver
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '详情':
            self.logstu.info(u'详情')
            self.saveSalesman()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '新增':
            self.logstu.info(u'新增')
            self.saveSalesman()
            self.logstu.info(u'新增end')
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '查询':
            self.logstu.info(u'查询')
            self.selectSalesman()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '角色维护':
            self.logstu.info(u'角色维护')
            self.setPermissions()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '首次登录':
            self.logstu.info('首次登录')
            #self.pub.noOneLogin(self.dict_data['登录地址'], self.dict_data['登录用户'], self.dict_data['登录密码'])
            self.pub.onelogin_setpwd(self.dict_data['登录地址'], self.dict_data['登录用户'], self.dict_data['登录密码'], self.dict_data['输入值1'])
            self.assertTrue(self.driver.find_element_by_link_text('退出系统').is_displayed(), '登录后未找到 退出系统 按钮！')
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '变更结果':
            self.logstu.info(u'查看变更结果')
            self.change_result()
    #查看变更结果，add by limeng
    def change_result(self):
        #获取身份证号码
        cert_id = self.dict_data['查询条件1'].split('|')[1]
        #cert_id = '440233199103014036'
        #获取预期结果
        date = self.dict_data['预期结果']
        date_dict = eval(date)
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.click_btn(driver.find_element_by_id('FilterIconPlus'))
        time.sleep(2)
        #btn = driver.find_ele
        self.pub.select_set(2,1,cert_id)
        time.sleep(1)
        self.pub.select_btn(u'查询')
        self.pub.comeinifm('right','myiframe0')
        time.sleep(3)
        #点击查看详情
        self.pub.click_btn(driver.find_element_by_name("R0F0") )
        #self.pub.table_RowClick(0)
        self.pub.comeinifm('right')
        self.pub.thread_btn('详情')
        time.sleep(2)
        self.pub.comeinifm('ObjectList','myiframe0')
        # 获取值后，关闭页面.获取预期结果并校验
        phone_no = driver.find_element_by_css_selector("input[name='R0F23']").get_attribute('value')
        email_address = driver.find_element_by_css_selector("input[name='R0F24']").get_attribute('value')
        time.sleep(2)
        self.pub.winClose()
        check_list = {'电子邮箱': email_address, '移动电话': phone_no}
        if check_list == date_dict:
            self.logstu.info(check_list.__str__() + u'等于' + date_dict.__str__())
            self.logstu.info(u"变更的数据和查看的结果一致，变更正确，测试通过")
            pass
        else:
            self.logstu.info(check_list.__str__() + u'不等于' + date_dict.__str__())
            self.logstu.info(u"变更的数据和查看的结果不一致，测试失败")
            raise Exception



    # 保存销售人员信息
    def saveSalesman(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right', 'myiframe0')
        users = ''
        usernum = self.pub.table_getRowsCount()
        if usernum > 0:
            self.pub.table_th_sort('用户编号', 'fx')
            users = self.pub.table_getValue2(1, '用户编号')
            self.assertGreater(usernum, 0, '没有查询到用户数据。')
            self.pub.table_RowClick(1)
            self.pub.table_RowCheckBox(1)
            #self.logstu.debug('反序查询最后一个用户编号为：%s' % (self.pub.all_type_to_encode(users)))

        self.pub.comeinifm('right')
        oldhs = driver.window_handles
        self.pub.thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])
        self.pub.goNewWindow(oldhs)
        #self.pub.setEditTableValues(self.dict_data, 'ObjectList', 'myiframe0')
        self.pub.setEditTableValueFast(self.dict_data, 'ObjectList', 'myiframe0')
        self.pub.comeinifm('ObjectList')
        driver.set_script_timeout(1)
        #self.pub.thread_btn('保存')
        #driver.execute_script("document.getElementsByName('ObjectList')[0].contentWindow.saveRecord()")
        driver.execute_script("window.saveRecord()")
        self.logstu.debug('js save end!')
        self.logstu.debug(driver.window_handles)

        self.pub.goLastOneWindow()
        driver.set_script_timeout(30)
        #check create user
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right', 'myiframe0')
        newusernum = self.pub.table_getRowsCount()
        if usernum == 0 and newusernum == 1:
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], self.pub.table_getValue2(1, '用户编号'), self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
        elif self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '新增':
            self.pub.table_th_sort('用户编号', 'fx')
            newusers = self.pub.table_getValue2(1, '用户编号')
            self.logstu.debug(type(self.actdb.casetitle_cn['执行结果']))
            self.logstu.debug(type(newusers))
            self.logstu.debug(self.dict_data)
            self.logstu.debug(type(self.dict_data['test_id']))
            self.logstu.debug('新增前反序查询最后一个用户编号为：%s' % (self.pub.all_type_to_encode(users)))
            self.logstu.debug('新增后反序查询最后一个用户编号为：%s' % (self.pub.all_type_to_encode(newusers)))
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], newusers, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.assertNotEqual(newusers, users, '新增失败，新增前后最后一个用户的编号没有变化')



    # 查询数据，并将操作类型第3个描述的列的值返回，并写入excel
    def selectSalesman(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        self.pub.comeinifm('right', 'myiframe0')
        count = self.pub.table_getRowsCount()
        self.assertNotEqual(0, count, u'未查询到数据')
        self.pub.table_RowCheckBox(1)
        rul = self.pub.table_getValue2(1, self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2])
        self.logstu.info(self.pub.all_type_to_unicode(rul))
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        return rul

    # 设置用户权限
    def setPermissions(self):
        driver = self.driver
        self.selectSalesman()
        self.pub.comeinifm('right')
        oldhs = driver.window_handles
        driver.set_page_load_timeout(1)
        try:
            self.pub.thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])
        except TimeoutException as e:
            self.logstu.debug(e)
        driver.set_page_load_timeout(30)
        self.pub.goNewWindow(oldhs)

        self.pub.comeinifm('ObjectList')
        qxstrs = self.pub.all_type_to_encode(self.dict_data["输入值1"]).split('|')
        for qxstr in qxstrs:
            self.set_QuanXian(qxstr)
        driver.find_element(*self.savebtn_by).click()
        self.logstu.debug(self.pub.close_alert_and_get_its_text())
        alert2 = self.pub.close_alert_and_get_its_text() # 角色操作成功
        self.logstu.debug(alert2)
        time.sleep(1)
        self.assertNotEqual(-1, self.pub.all_type_to_encode(alert2).find('角色操作成功'), alert2)
        time.sleep(1)
        self.pub.winClose2()


