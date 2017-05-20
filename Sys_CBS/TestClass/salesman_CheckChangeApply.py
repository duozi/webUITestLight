# -*- coding: utf-8 -*-

from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from Sys_CBS.PageObj.salesmanFunction import SalesmanFunction
import unittest, time

#create by limeng
class SalesmanCheckChangeApply(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    row =""          #接收main脚本传送的当前处理的行数


    def setUp(self):
        #self.driver = self.comm.get_browserdrvie('Chrome')
        self.driver = self.mainWebDr
        self.driver.implicitly_wait(30)
        self.pub = PublicAct(self.driver)
        self.salesman = SalesmanFunction(self.driver)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.execldata = ""
        self.filepath = ""
        #进入具体菜单
        #self.comm.goto_menu(self.driver,self.row)
        self.pub.goto_menu(self.dict_data)

    def test_SalesmanChangeApply(self):
        driver = self.driver
        if self.dict_data["操作类型"].encode('utf8') == '变更审核':
            self.logstu.info(u'变更审核')
            self.change_approval()
        if self.dict_data["操作类型"].encode('utf8') == '变更审核不通过':
            self.logstu.info(u'变更审核不通过')
            self.change_approval_fail()

    def change_approval(self):
        cert_id = self.dict_data['查询条件1'].split('|')[1]
        #cert_id = '37012619860510622X'
        driver = self.driver
        self.pub.comeinifm('left')
        self.pub.click_btn(driver.find_element_by_css_selector("a[title='待处理申请']"))
        self.pub.click_btn(driver.find_element_by_id("text2"))
        self.logstu.info(u"批量获取任务")
        self.pub.comeinifm('right')
        btn = self.pub.click_btn(driver.find_element_by_xpath("//table[@id='ListTable']"))
        self.pub.click_btn(driver.find_element_by_xpath("//tr[@id='ButtonTR']//span[@title='批量获取任务']//div[@class='btn_text']"))
        text = self.pub.close_alert_and_get_its_text()
        self.logstu.info(text)
        try:
            text = self.pub.close_alert_and_get_its_text()
        except Exception as e:
            self.logstu.info(e)
        time.sleep(2)
        self.pub.comeinifm('right','myiframe0')
        self.pub.click_btn(driver.find_element_by_css_selector("input[value='%s']" % cert_id))
        self.pub.comeinifm('right')
        self.pub.thread_btn2(driver.find_element_by_xpath("//tr[@id='ButtonTR']//span[@title='签署意见']//div[@class='btn_text']"))
        time.sleep(2)
        self.pub.comeinifm('ObjectList', 'myiframe0')
        #签署意见，同意
        date = 'OK'
        self.pub.input_text(driver.find_element_by_css_selector("textarea[id='R0F4']"),date)
        self.pub.comeinifm('ObjectList')
        time.sleep(2)
        self.pub.table_BtnClick_NoSetTimeOut('保存')
        self.pub.winClose()
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.click_btn(driver.find_element_by_css_selector("input[value='%s']" % cert_id))
        time.sleep(2)
        # 提交并选择通过
        self.pub.comeinifm('right')
        self.pub.thread_btn2(driver.find_element_by_xpath("//tr[@id='ButtonTR']//span[@title='提交']//div[@class='btn_text']"))
        s = driver.find_element_by_css_selector("select[class='select1']")
        s.find_element_by_xpath("//option[@value='通过']").click()
        time.sleep(2)
        self.pub.thread_btn2(driver.find_element_by_css_selector("td[class='button'][id='buttonmiddletd21']"))
        windows = driver.window_handles
        time.sleep(1)
        self.pub.close_alert_and_get_its_text()
        for i in range(0,10):
            time.sleep(2)
            windows1 = driver.window_handles
            if len(windows)-1 == len(windows1):
                self.pub.goLastOneWindow()
                self.pub.close_alert_and_get_its_text()
                break
        time.sleep(5)

    def change_approval_fail(self):
        driver = self.driver
        cert_id = self.dict_data['查询条件1'].split('|')[1]
        reson = self.dict_data['查询条件2'].split('|')[1]
        cert_id = '370124199301051524'
        self.pub.comeinifm('left')
        self.pub.click_btn(driver.find_element_by_css_selector("a[title='待处理申请']"))
        self.pub.click_btn(driver.find_element_by_id("text2"))
        self.logstu.info(u"批量获取任务")
        self.pub.comeinifm('right')
        btn = self.pub.click_btn(driver.find_element_by_xpath("//table[@id='ListTable']"))
        self.pub.click_btn(
            driver.find_element_by_xpath("//tr[@id='ButtonTR']//span[@title='批量获取任务']//div[@class='btn_text']"))
        text = self.pub.close_alert_and_get_its_text()
        self.logstu.info(text)
        try:
            text = self.pub.close_alert_and_get_its_text()
        except Exception as e:
            self.logstu.info(e)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.click_btn(driver.find_element_by_css_selector("input[value='%s']" % cert_id))
        time.sleep(2)
        # 提交并选择通过
        self.pub.comeinifm('right')
        self.pub.thread_btn2(driver.find_element_by_xpath("//tr[@id='ButtonTR']//span[@title='提交']//div[@class='btn_text']"))
        s = driver.find_element_by_css_selector("select[class='select1']")
        s.find_element_by_xpath("//option[@value='拒绝']").click()
        time.sleep(1)
        #选择不通过原因
        s1 = driver.find_element_by_css_selector("select[id='PhaseAction']")
        s1.find_element_by_xpath("//option[@value='%s']" %reson ).click()
        self.pub.thread_btn2(driver.find_element_by_css_selector("td[class='button'][id='buttonmiddletd21']"))
        windows = driver.window_handles
        time.sleep(1)
        self.pub.close_alert_and_get_its_text()
        for i in range(0, 10):
            time.sleep(2)
            windows1 = driver.window_handles
            if len(windows) - 1 == len(windows1):
                self.pub.goLastOneWindow()
                self.pub.close_alert_and_get_its_text()
                break
        time.sleep(5)

