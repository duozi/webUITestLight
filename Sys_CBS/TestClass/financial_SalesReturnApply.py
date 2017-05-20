# -*- coding: utf-8 -*-
import unittest,time
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from Sys_CBS.PageObj.jFunction import Function

class FinancialSalesReturnApply(unittest.TestCase):
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

    def test_FinancialSalesReturnApply(self):
        driver = self.driver
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]) == '退货登记':
            self.logstu.info(u'退货流程')
            self.ReturnApply()


    def ReturnApply(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.select_set(4, 4, u'退货审批通过')
        time.sleep(1)
        self.pub.select_btn(u'查询')
        self.pub.comeinifm('right','myiframe0')
        trs = driver.find_elements(*self.pub.table_tr)
        self.logstu.debug(u'行数：'+str(len(trs)))
        try:
            for num in range(1,10):
                tds = driver.find_elements(*self.pub.table_tr)[num +1].find_elements_by_tag_name('td')
                input = tds[9].find_element_by_tag_name('input')
                self.logstu.debug(u'客户需支付金额==========：' + input.get_attribute('value'))
                if input.get_attribute('value') == ('0.00'):
                    self.logstu.debug(u'客户需支付金额：'+input.get_attribute('value'))
                    input.click()
                    break
            # self.Fun.RowClick(1)
            driver.switch_to_default_content()
            self.pub.comeinifm('right')
            time.sleep(1)
            self.pub.thread_btn(u'退货确认')
            time.sleep(1)
            alert_text = self.pub.is_alert_and_close_and_get_text2()
            self.logstu.debug(alert_text.strip('!'))
            self.assertEquals(alert_text.strip('!'), self.dict_data['预期结果'])
        except IndexError as e:
                self.logstu.error(e)
                self.logstu.error(u'无可用于退货确认的数据')






