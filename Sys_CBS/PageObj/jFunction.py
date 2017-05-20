# -*- coding: utf-8 -*-
from Sys_CBS.PageObj.commFunction import CommFunction
from Sys_CBS.PageObj.lyElementsOperation import PublicAct


class Function():
    def __init__(self, driver):
        self.driver = driver
        #self.dict_data = test_dict_data  # 接收excel用例参数
        self.comm = CommFunction()
        self.pub = PublicAct(self.driver)

    # 选择行数
    def RowClick(self, rownum):
        driver = self.driver
        table_tr = driver.find_elements(*self.pub.table_tr)
        table_td = table_tr[rownum + 1].find_elements_by_tag_name('td')
        table_td[rownum].click()

        #testcase中 执行结果 为主键，用该值在查询列表中查询，可以得到唯一一列数据
        #查询写入到执行结果列中的值是否存在
    def get_SearchResult(self):
        driver = self.driver

        Value = self.dict_data["执行结果"].encode('utf-8')
        print "主键备注" + Value
        driver.switch_to_frame("right") #进入 right 这个框架
        #判断 + 号按钮是否隐藏，如果隐藏，点击 + 按钮展开
        Select = driver.find_element_by_id("FilterIconPlus")
        if Select.is_displayed():
            Select.click()
        #将 保存在 用例中的产品系列编号作为查询条件在列表中查询
        trs = driver.find_element(self.selectelement.selectList)
        print trs
        #driver.find_elements(driver.find_element_by_tag_name(""))
        condition = driver.find_element_by_id("DF2_OP_ID")
        condition.find_element_by_xpath("//option[@value = 'EqualsString']").click()
        driver.find_element_by_id("DF2_1_INPUT").send_keys(Value)

        #driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td/input[1]").click()
        driver.switch_to_default_content()
        print "1111111111111111111111111111111111"

    def get_ifm(self,ifmname):
        driver = self.driver
        ifm = driver.find_element_by_name(ifmname)
        for i in range(0,5):
            if ifm is False:
                driver.find_element_by_name(ifm)
                print i,ifmname
        driver.switch_to_frame(ifm)


















    #def PublicWriteResult(self,):
