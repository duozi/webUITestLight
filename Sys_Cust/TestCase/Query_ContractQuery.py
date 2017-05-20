# -*- coding: utf-8 -*-
# 小牛分期 合同查询页面是否有数据用例实现
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from script.testunite.comm.lyElementsOperation import PublicAct
from script.testunite.comm.getElements import SearchElement
from script.testunite.comm.getElements import FindElement
from script.testunite.comm.getElements import FindTableData
from script.testunite.comm.logger import Logger
from script.testunite.comm.salesmanFunction import SalesmanFunction
import unittest, time, re,threading, httplib

class QueryContractQuery(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
    logstu = ""  # 接收main脚本传递来的写log的对象
   # right_between_btn = [u'销售商户信息查询',u'客户信息查询',u'清除']

    #审批未通过, 未通过原因 控件
   # approval_nopass_reason_sel = (By.CSS_SELECTOR,"select[id=\"R0F0\"]")
    #审批未通过, 未通过备注 控件
    #approval_nopass_remarks_sel = (By.CSS_SELECTOR,"textarea[id=\"R0F1\"]")
    #页面控件元素别
    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_QueryContractQuery(self):
        driver = self.driver
        #确认是否需要登录
#        if (self.dict_data["登录用户"] <> "" and self.dict_data["登录密码"] <> ""):
#            self.comm.goto_menu(driver,self.row)
        #searchAct_class = searchAct(self)
        #输入姓名
#        customerNamelabel,customerName = self.comm.split_str(self.dict_data["查询条件2"])
        #输入联系方式
#        mobileNumberlabel,mobileNumber = self.comm.split_str(self.dict_data["查询条件3"])
       #输入身份证号
#        idCardlabel,idCard = self.comm.split_str(self.dict_data["查询条件4"])
        time.sleep(3)
       #输入合同编号
        self.logstu.debug('查询条件1：%s' % (self.dict_data['查询条件1'].split('|')[1]))
        idArtificialno = self.comm.split_str(self.dict_data["查询条件1"])
#        idArtificialno = 'FP19d62016052700000548'
        driver.find_element(*SearchElement.idArtificialnoEdit).send_keys(idArtificialno)
        #点击提交按扭
        time.sleep(3)
        driver.find_element(*SearchElement.submitButton).click()
        time.sleep(30)
        #调用详情查看方法确认列表有值
        ContractId = driver.find_element(*FindElement.ContractId).text
        self.logstu.debug('ContractId：%s' % (ContractId))
        table_data = driver.find_element(*FindTableData.TableData).text
        self.logstu.debug('table_data：%s' % (table_data))
        if ContractId != 'idArtificialno':
            if table_data == '':
                self.confirm_test()
        else:
            pass

    #确认页面两个table列表中有值,否则执行该方法让该用例执行失败
    def confirm_test(self):
        self.logstu.debug('SF：%s' % (SF))

    def thread_btn(self,btnname):
        try:
            self.pub.table_BtnClick(btnname)
        except TimeoutException as e:
            print e

    def thread_main(self,btnname):
        threads = []
        t1 = threading.Thread(target=self.thread_btn,args=(btnname,))
        t1.setDaemon(True)
        t1.start()

    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()