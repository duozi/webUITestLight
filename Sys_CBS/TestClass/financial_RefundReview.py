# -*- coding: utf-8 -*-
import unittest,time
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from Sys_CBS.PageObj.jFunction import Function

class FinancialRefundReview(unittest.TestCase):
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象


    def setUp(self):
        # self.driver = self.comm.get_browserdrvie('Chrome')
        self.driver = self.mainWebDr
        self.driver.implicitly_wait(6)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.execldata = ""
        self.filepath = ""
        self.pub = PublicAct(self.driver)
        self.Fun = Function(self.driver)

        # 进入具体菜单
        self.driver.implicitly_wait(6)
        self.comm.goto_menu(self.driver,self.row)
        self.logstu.debug(self.row)
        # 获取最后一级的菜单名
        menuname = self.comm.get_last_menuname(self.row)
        self.logstu.debug(menuname)

    def test_FinancialRefundReview(self):
        driver = self.driver
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]) == '退款复核':
            self.logstu.info(u'退款复核流程')
            self.RefundReview()


    def RefundReview(self):
        driver = self.driver
        self.pub.comeinifm('right')
        value = self.pub.all_type_to_encode(self.dict_data['查询条件1'].split('|')[1])
        self.pub.select_set(1,4,value)
        time.sleep(1)
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()
        self.pub.comeinifm('right','myiframe0')
        time.sleep(1)
        self.Fun.RowClick(1)
        driver.switch_to_default_content()
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'退款复核')
        time.sleep(1)
        self.pub.setEditTableValues(self.dict_data,'myiframe0')
        driver.switch_to_default_content()
        self.pub.thread_btn(u'审核通过')
        alert_text = self.pub.is_alert_and_close_and_get_text2()
        self.logstu.debug(alert_text.strip(u'！'))
        self.assertEquals(alert_text.strip(u'！'),self.dict_data['预期结果'])






