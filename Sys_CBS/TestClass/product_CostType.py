# -*- coding: utf-8 -*-

from Sys_CBS.PageObj.lyElementsOperation import PublicAct
import unittest, time, re

#create by limeng
#2016.8.16
class ProductCostType(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的


    def setUp(self):
        self.driver = self.mainWebDr
        self.accept_next_alert = True
        self.pub = PublicAct(self.driver)
        # 进入具体菜单
        self.driver.implicitly_wait(6)
        self.pub.goto_menu(self.dict_data)
        self.verificationErrors = []

    def test_ProductCostType(self):
        driver = self.driver
        if self.dict_data["操作类型"] == '新增费用':
            self.logstu.info(self.dict_data["操作类型"])
            self.new_cost()
        if self.dict_data["操作类型"] == '启用费用':
            self.logstu.info(self.dict_data["操作类型"])
            self.cost_start_stop("on")
        if self.dict_data["操作类型"] == '停用费用':
            self.logstu.info(self.dict_data["操作类型"])
            self.cost_start_stop("off")
        if self.dict_data["操作类型"] == '修改费用参数':
            self.logstu.info(self.dict_data["操作类型"])
            self.cost_parameter_modify()
        if self.dict_data["操作类型"] == '修改费用基本信息':
            self.logstu.info(self.dict_data["操作类型"])
            self.cost_info_modify()

    def new_cost(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'新增费用')
        ###进入到新增界面
        time.sleep(2)
        self.pub.input_values(self.dict_data,"product",'ObjectList','myiframe0')
        self.pub.comeinifm('ObjectList')
        self.pub.thread_btn(u"保存")
        time.sleep(1)

    def cost_start_stop(self,act):
        driver = self.driver
        self.pub.comeinifm('right','myiframe0')
        self.pub.table_text_clicks(self.dict_data)
        self.pub.comeinifm('right')
        if (act == "on" ):
            self.pub.timeoutBtnClick(u"启用")
            self.pub.alert_accept_dismiss("accept")
        elif (act == "off" ):
            self.pub.timeoutBtnClick(u"停用")
            self.pub.alert_accept_dismiss("accept")
        self.logstu.info("alert text is "+self.pub.close_alert_and_get_its_text())
        time.sleep(1)

    def cost_parameter_modify(self):
        driver = self.driver
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_text_clicks(self.dict_data)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u"费用详情")
        self.pub.input_values(self.dict_data,"product_info",'ObjectList','myiframe0','TermParaView','myiframe0')
        self.pub.comeinifm('ObjectList','myiframe0','TermParaView')
        self.pub.timeoutBtnClick(u"保存")
        self.pub.winClose()
        time.sleep(1)

    def cost_info_modify(self):
        driver = self.driver
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.table_text_clicks(self.dict_data)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u"费用详情")
        self.pub.input_values(self.dict_data, "product_info", 'ObjectList', 'myiframe0')
        self.pub.comeinifm('ObjectList')
        self.pub.timeoutBtnClick(u"保存")
        self.pub.winClose()
        time.sleep(1)