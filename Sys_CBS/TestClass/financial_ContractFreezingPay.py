# -*- coding: utf-8 -*-
import unittest,time
from Sys_CBS.PageObj.lyElementsOperation import PublicAct

class FinancialContractFreezingPay(unittest.TestCase):
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
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
        # self.Fun = Function()

        # 进入具体菜单
        self.driver.implicitly_wait(6)
        self.comm.goto_menu(self.driver,self.row)
        self.logstu.debug(self.row)
        # 获取最后一级的菜单名
        menuname = self.comm.get_last_menuname(self.row)
        self.logstu.debug(menuname)

    def test_FinancialContractFreezingPay(self):
        driver = self.driver
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]) == '财务冻结':
            self.logstu.info(u'财务冻结流程')
            self.FinancialFreeze()

    def FinancialFreeze(self):
        driver = self.driver
        self.logstu.debug(u'=========解除冻结合同付款开始============')
        time.sleep(2)
        driver.switch_to_default_content()
        self.pub.leftMenuVagueClick(u'已冻结合同', 'left')
        self.pub.comeinifm('right', 'myiframe0')
        self.RowClick(1)
        ContractNO = self.WriteFile(1)
        driver.switch_to_default_content()
        self.pub.comeinifm('right')
        time.sleep(1)
        self.pub.thread_btn(u'解除冻结合同付款指令')
        time.sleep(1)
        alert_text1 = self.pub.is_alert_and_close_and_get_text2()
        self.logstu.debug(alert_text1.strip('!'))
        time.sleep(3)
        self.pub.leftMenuVagueClick(u'待冻结合同', 'left')
        self.pub.comeinifm('right')
        self.pub.select_set(1, 4, ContractNO)
        self.pub.select_btn(u'查询')
        time.sleep(3)
        driver.switch_to_default_content()
        self.pub.comeinifm('right', 'myiframe0')
        self.RowClick(1)
        driver.switch_to_default_content()
        #################冻结付款
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'冻结合同付款指令')
        time.sleep(1)
        alert_text = self.pub.is_alert_and_close_and_get_text2()
        self.logstu.debug(alert_text.strip('!'))
        # driver.switch_to_default_content()
        self.logstu.debug(u'=========冻结合同付款完成============')
        driver.switch_to_default_content()
        ########## 验证用例是否执行成功
        self.assertEqual(self.dict_data['预期结果'],alert_text.strip('!'))
        self.logstu.debug('end=============')



# 选择行数
    def RowClick(self,rownum):
        driver = self.driver
        table_tr = driver.find_elements(*self.pub.table_tr)
        table_td = table_tr[rownum +1].find_elements_by_tag_name('td')
        table_td[rownum].click()

#将合同编号写入excel中，并返回合同编号
    def WriteFile(self,rownum):
        driver = self.driver
        table_td = driver.find_elements(*self.pub.table_tr)[rownum +1].find_elements_by_tag_name('td')
        str_in = table_td[rownum].find_element_by_tag_name('input').get_attribute('value')
        self.logstu.debug(u'当前合同编号：' + str_in)
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], str_in, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        return str_in