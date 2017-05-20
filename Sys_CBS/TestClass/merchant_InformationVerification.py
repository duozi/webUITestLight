# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
import unittest, time, re

class MerchantInformationVerification(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    row =""          #接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象

    #查询菜单的控件
    mentelement = (By.LINK_TEXT,'信息验证')
    #页面"验证"控件
    verifelement = (By.CSS_SELECTOR,'div[class="btn_text"]')
    #页面"下一步"控件

    #页面"客户手机验证码"输入框控件

    #页面"销售手机验证码"输入框控件

    #页面控件元素别
    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_MerchantInformationVerification(self):
        driver = self.driver
        #driver =webdriver.Firefox()
        #获取操作类型
        opt = self.dict_data["操作类型"].split("|")
        if opt[0] == u'验证':
            self.logstu.info(u"商户后台信息验证流程")
            self.informationVerification()
        #将预期结果和执行结果做比对, 并记录到验证结果中
        self.comm.write_reslut(self.row)

    #商户后台 信息验证操作步骤
    def informationVerification(self):
        self.logstu.debug(u"开始进行商户后台信息查询操作")
        driver = self.driver
        #确认是否需要登录
        firstment = driver.find_element(*self.mentelement)
        ActionChains(driver).move_to_element(firstment).perform()
        foxments = driver.find_elements(*self.mentelement)
        for alinkelemnt in foxments:
            alinkelemnt.click()
        self.logstu.debug("--------------------------------------------")
        self.pub.setEditTableValueFast(self.dict_data,'right','myiframe0')
        self.logstu.info(u'点击验证按钮')
        self.pub.comeinifm('right')
        self.pub.table_BtnClick(u'验证')
        time.sleep(1)
        verifalert = self.pub.is_alert_and_close_and_get_text()
        if verifalert == False or verifalert =='数据保存成功' or verifalert == '系统正在处理数据,请稍等...':
            self.pub.table_BtnClick(u'下一步')
            driver.implicitly_wait(5)
            self.pub.table_BtnClick(u'确定')
            #self.pub.is_alert_and_close_and_get_text()
            time.sleep(0.5)
            while True:
                resluttext = self.pub.is_alert_and_close_and_get_text()
                self.logstu.debug(resluttext)
                if resluttext <> False:
                    break
            self.logstu.info(resluttext)
            self.comm.write_file(resluttext,self.row,self.comm.get_key_cell_col("执行结果"))
        else:
            self.logstu.debug(u"点击验证按扭: " + verifalert)
            self.comm.write_file(verifalert,self.row,self.comm.get_key_cell_col("执行结果"))

    def tablebtn(self,btnname,*imf):
        driver = self.driver
        self.pub.comeinifm(*imf)
        tablebtns = driver.find_elements(*self.verifelement)
        for btn in tablebtns:
            if btn.text == '验证':
                btn.click()



    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)
