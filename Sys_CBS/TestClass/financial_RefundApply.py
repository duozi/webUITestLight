# -*- coding: utf-8 -*-
import unittest,time
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from Sys_CBS.PageObj.jFunction import Function
from selenium.webdriver.common.by import By

class FinancialRefundApply(unittest.TestCase):
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
    logstu = ""  # 接收main脚本传递来的写log的对象

    SerialNumber = (By.CSS_SELECTOR, 'input[name="R0F0"]')
    CustomerNumber = (By.CSS_SELECTOR, 'input[name="R0F1"]')


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

    def test_FinancialRefundApply(self):
        driver = self.driver
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]) == '退款登记':
            self.logstu.info(u'退款登记流程')
            self.RefundApply()


    def RefundApply(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.select_set(2,4,u'审批通过')
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()
        self.pub.comeinifm('right','myiframe0')
        self.Fun.RowClick(1)
        driver.switch_to_default_content()
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'退款登记')
        self.pub.setEditTableValues(self.dict_data,'myiframe0')
        serialnum = driver.find_element(*self.SerialNumber).get_attribute('value')
        customernumber = driver.find_element(*self.CustomerNumber).get_attribute('value')
        self.logstu.debug(u'流程号：'+serialnum)
        self.logstu.debug(u'客户号：' + customernumber)
        driver.switch_to_default_content()
        time.sleep(1)
        self.pub.thread_btn(u'确定')
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], customernumber, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)

        #退款登记成功
        time.sleep(1)
        alert_text = self.pub.is_alert_and_close_and_get_text2()
        self.logstu.debug(alert_text.strip('!'))
        self.assertEquals(alert_text.strip('!'), self.dict_data['预期结果'])




