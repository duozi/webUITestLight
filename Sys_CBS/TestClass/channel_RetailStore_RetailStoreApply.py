# -*- coding: UTF-8 -*-

import unittest
import time,os
from Sys_CBS.PageObj.commFunction import CommFunction
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException,UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class ChannelRetailStoreRetailStoreApply(unittest.TestCase):
    '''渠道管理  商户门店管理  商户门店准入申请'''
    # 产品管理-商品类型：增删改查
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    actdb = None # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
    logstu = ""  # 接收main脚本传递来的写log的对象

    link_a = (By.TAG_NAME, 'a')  # 门店详情  门店附件信息
    select_commit = (By.ID, 'PhaseOpinion1')  # 意见选择列表
    select1_commit = (By.ID, 'PhaseAction')   # 动作选择列表
    btn_commit = (By.ID, 'buttonmiddletd21') # 提交按钮
    btn_giveup = (By.ID, 'buttonmiddletd22') # 放弃按钮

    def link_a_go(self, aName):
        alla = self.driver.find_elements(*self.link_a)
        for onea in alla:
            if self.pub.all_type_to_encode(onea.text) == self.pub.all_type_to_encode(aName):
                onea.click()
                return
        raise Exception('未找到按钮：' + self.pub.all_type_to_encode(aName))

    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.logstu.info(self.pub.all_type_to_encode(self.dict_data["案例名称"])+ '---' + self.pub.all_type_to_encode(self.dict_data["案例详情"]))
        # 进入具体菜单项
        try:
            self.pub.goto_menu(self.dict_data)
        except UnexpectedAlertPresentException as e:
            self.logstu.debug(e)
            self.logstu.debug(self.pub.is_alert_and_close_and_get_text())
        self.pub.leftMenuClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[0], 'left')
        self.dict_data = self.pub.testSateOnlySet(self.dict_data)
        self.logstu.debug(self.dict_data)

    # 测试流程
    def test_RetailStoreApply(self):
        driver = self.driver
        act = self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1]
        if act == '新增申请' or act == '申请详情':
            self.logstu.info('测试流程 %s'%(act))
            if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '基本信息':
                self.createRetailStoreApply()
            if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '关联门店信息':
                self.createRetailStoreChild()
        if act == '提交' or act == '删除':
            self.logstu.info(act)
            self.commit_StoreApply()
        if act == '生成门店代码':
            self.logstu.info(u'生成门店代码')
            self.produced_StoreNum()

    # 新增商户
    def createRetailStoreApply(self):
        # 打开详情页面
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        if self.pub.table_getRowsCount() > 0:
            self.pub.table_RowClick(1)
        # 打开商户新增或详情页面
        self.pub.comeinifm('right')
        self.pub.thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])

        # 编辑详情页，最后按下保存和返回
        self.pub.setEditTableValueFast(self.dict_data, 'ObjectList', 'right', 'myiframe0')
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.thread_btn(u'保存')
        self.pub.winClose()
        shname = self.pub.all_type_to_encode(self.pub.testDateSelect(self.dict_data, '商户名称|'))
        if shname != '':
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'],shname.split('|')[1],self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)

    # 关联门店信息，新增门店
    def createRetailStoreChild(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)
        # 打开详情页面
        self.pub.comeinifm('right')
        self.pub.thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])

        self.pub.logstu.debug(driver.title)
        # 选择左侧菜单关联门店信息，在按下新增按钮
        self.pub.leftMenuClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2], 'ObjectList', 'left')

        # 窗口换到新增门店窗口
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[3] == '新增':
            self.pub.comeinifm('ObjectList', 'right')
            self.pub.thread_btn(u'新增')
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[3] == '详情':
            if self.dict_data["操作对象"] != '': #self.pub.comeinifm('ObjectList', 'right', 'myiframe0')
                self.pub.comeinifm('ObjectList', 'right', 'myiframe0')
                rows = self.pub.table_getRowsCount()
                if rows < 1:
                    self.assertLess(0, rows, '没有可用编辑的门店信息')
                if len(self.dict_data["操作对象"].split('|')) < 2:
                    self.assertEqual(2, len(self.dict_data["操作对象"].split('|')), '数据格式不正确，请检查testcase数据。')
                flag = False
                for men in range(1, rows + 1):
                    menname = self.pub.all_type_to_encode(self.pub.table_getValue2(men, self.dict_data["操作对象"].split('|')[0]))
                    if menname == self.pub.all_type_to_encode(self.dict_data["操作对象"].split('|')[1]):
                        self.pub.table_RowClick(men)
                        flag = True
                        break
                if flag == False:
                    self.assertTrue(flag, '没有选择被编辑的门店，无法继续操作。')
                self.pub.comeinifm('ObjectList', 'right')
                self.pub.thread_btn(u'详情')
            else:
                self.assertNotEqual('',self.dict_data["操作对象"], '测试数据中没有被编辑门店信息，请检查testcase数据。')
        # 编辑门店详情，最后按下保存和返回
        self.pub.setEditTableValueFast(self.dict_data, 'ObjectList', 'tab_T01_iframe_TS0', 'myiframe0')

        shname = self.pub.all_type_to_encode(self.pub.testDateSelect(self.dict_data, '门店名称|'))
        if shname != '':
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % \
                        (self.actdb.casetitle_cn['执行结果'], shname.split('|')[1], self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
        if self.pub.all_type_to_encode(self.pub.testDateSelect(self.dict_data, '门店附件信息')) != '':
            driver.switch_to_window(driver.current_window_handle)
            self.pub.comeinifm('ObjectList')
            self.link_a_go('门店附件信息')
            # 选择左侧菜单上传门店照
            fujianmenu = self.pub.testDateSelectList(self.dict_data, '门店附件信息')
            for fujian in fujianmenu:
                #driver.switch_to_default_content()
                self.pub.leftMenuClick(fujian.split('-')[1], 'ObjectList', 'tab_T01_iframe_TS1', 'frameleft', 'left')
                self.pub.comeinifm('ObjectList', 'tab_T01_iframe_TS1', 'frameright', 'rightup')
                oldhs = driver.window_handles
                self.pub.thread_btn('上传附件')
                self.pub.goNewWindow(oldhs)
                self.pub.comeinifm('ObjectList')

                img_num = len(fujian.split('-'))
                if img_num < 3:
                    self.assertEqual('xxx.jpg', '', '测试数据中未找到上传的图片名称，请核对testcase数据。')
                for num in range(2, img_num):
                    upload_rult = self.pub.all_type_to_encode(self.pub.uploadfile(fujian.split('-')[num]))
                    self.pub.logstu.debug('上传文件结果：' + upload_rult)
                    if upload_rult.find('请选择一个文件名') > -1:
                        self.assertNotEqual(upload_rult.find('请选择一个文件名'), -1, upload_rult)
                    if upload_rult.find('数据插入失败') > -1:
                        self.assertNotEqual(upload_rult.find('数据插入失败'), -1, upload_rult)
                driver.switch_to_default_content()
                self.pub.winClose()  # 关闭上传文件弹窗
            self.pub.comeinifm('ObjectList')
            self.link_a_go('门店详情')
        self.pub.comeinifm('ObjectList', 'tab_T01_iframe_TS0')
        self.pub.thread_btn(u'保存')
        self.pub.winClose2()
        self.pub.winClose2()

    # 查询操作
    def selectStore(self):
        driver = self.driver
        self.pub.comeinifm('right')
        #self.pub.select_sets(self.dict_data)
        #self.pub.select_btn(u'查询')
        self.pub.selectAutoSets(self.dict_data)
        driver.switch_to_default_content()

    # 门店准入申请提交，并验证是否提交成功
    def commit_StoreApply(self):
        driver = self.driver
        iflag = False
        shName = ''
        for i in range(1, 7):
            if self.dict_data['查询条件' + str(i)] != '':
                iflag = True
                break
        if iflag:
            self.selectStore()
        else:
            # 无查询条件时获取第一行的数据，被删除或提交的商户名称
            self.pub.comeinifm('right', 'myiframe0')
            shName = self.pub.all_type_to_encode(self.pub.table_getValue2(1, '商户名称'))
            self.logstu.debug('无查询条件，操作的商户名称为：%s' % (shName))
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)

        # 提交/删除
        self.pub.comeinifm('right')
        oldhs = driver.window_handles
        act = self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1]
        self.pub.thread_btn(act)
        if act == '删除':
            alertstr2 = ''
            for i in range(0, 10):
                alertstr = self.pub.all_type_to_encode(self.pub.is_alert_and_close_and_get_text2())
                if alertstr.find('您确定要删除该申请吗？') != -1:
                    time.sleep(0.5)
                    alertstr2 = self.pub.all_type_to_encode(self.pub.is_alert_and_close_and_get_text2())
                    break
                time.sleep(0.5)
            self.assertNotEqual(-1, alertstr2.find('成功'), '未找到删除成功提示信息。')
        if act == '提交':
            alerttxt = self.pub.is_alert_and_close_and_get_text2()
            self.logstu.debug(alerttxt)
            self.logstu.debug(u'切换到选择提交类型窗口，从select中选择提交申请.')
            phaseOpinion = driver.find_element(*self.select_commit)
            allOptions = phaseOpinion.find_elements_by_tag_name("option")
            for v in allOptions:
                if self.pub.all_type_to_encode(v.text) == self.pub.all_type_to_encode(self.dict_data["输入值1"]).split('|')[1]:#'提交申请':
                    driver.implicitly_wait(5)
                    for click_num in range(0,10):
                        try:
                            v.click()
                            driver.find_element(*self.select1_commit)
                            break
                        except Exception as e:
                            self.logstu.debug(e)
                            time.sleep(0.5)
                    break

            phaseAction = driver.find_element(*self.select1_commit)
            for v2 in range(0, 10):
                time.sleep(1)
                v3 = 0
                allOptions = phaseAction.find_elements_by_tag_name("option")
                for v in allOptions:
                    if self.pub.all_type_to_encode(v.text) == self.pub.all_type_to_encode(self.dict_data["输入值2"]).split('|')[1]:#'提交申请':
                        driver.implicitly_wait(5)
                        for click_num in range(0, 10):
                            try:v.click();break
                            except Exception as e:self.logstu.debug(e)
                            time.sleep(0.5)
                        v3 = 1
                        break
                if v3 == 1:
                    break
                time.sleep(1)

            if  self.pub.all_type_to_encode(self.dict_data["输入值3"]).split('|')[1]== '提交':
                driver.find_element(*self.btn_commit).click()
            elif self.pub.all_type_to_encode(self.dict_data["输入值3"]).split('|')[1]== '放弃':
                driver.find_element(*self.btn_giveup).click()
            else:
                self.assertEqual('提交/放弃',self.pub.all_type_to_encode(self.dict_data["输入值3"]).split('|')[1],'没有这个操作')

            commit_txt = self.pub.close_alert_and_get_its_text()
            self.logstu.debug(commit_txt)  # 该笔业务的下一阶段: 后台管理专员审核; 你确定提交吗？/ 您确定要放弃此次提交吗？
            driver.switch_to_window(driver.window_handles[0])
        # check 结果
        self.pub.goto_menu(self.dict_data)
        if shName == '':
            self.selectStore()
        else:
            self.pub.comeinifm('right')
            self.pub.selectAutoSet('商户名称','等于',shName)
            self.pub.select_btn(u'查询')
        self.pub.comeinifm('right', 'myiframe0')
        if act == '删除':
            self.assertEqual(self.pub.table_getRowsCount(), 0, u'删除失败，列表中该门店申请还存在。')
        elif self.pub.all_type_to_encode(self.dict_data["输入值3"]).split('|')[1] == '放弃':
            self.assertEqual(self.pub.table_getRowsCount(), 1, u'提交后选择放弃失败，列表中该门店申请不见了。')
        elif self.pub.all_type_to_encode(self.dict_data["输入值3"]).split('|')[1] == '提交':
            self.assertEqual(self.pub.table_getRowsCount(), 0, u'提交失败，列表中该门店申请还存在。')


    # 生成门店代码
    def produced_StoreNum(self):
        driver = self.driver
        self.selectStore()
        # 点击查询结果第一条数据
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_RowClick(1)

        self.pub.comeinifm('right')
        self.pub.base_thread_btn(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1])
        if self.pub.is_alert_present(self.driver):
            try:
                auditrl = self.pub.all_type_to_encode(self.pub.close_alert_and_get_its_text())
            except NoAlertPresentException as e:
                self.logstu.debug(e)
        okrl = self.pub.all_type_to_encode(self.dict_data["预期结果"])
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], auditrl, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        self.assertNotEqual(auditrl.find(okrl), -1, '审核预期结果：' + okrl + '  | 实际执行结果：' + auditrl)




