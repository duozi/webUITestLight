# -*- coding: utf-8 -*-

from Sys_CBS.PageObj.lyElementsOperation import PublicAct
import unittest, time, re

#create by limeng
#2016.8.16
class ProductConfigCommodityLoan(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的


    def setUp(self):
        self.driver = self.mainWebDr
        self.accept_next_alert = True
        #self.driver = webdriver.Firefox()
        #self.driver.implicitly_wait(30)
        self.pub = PublicAct(self.driver)
        # 进入具体菜单
        self.driver.implicitly_wait(6)
        self.pub.goto_menu(self.dict_data)
        self.verificationErrors = []

    def test_ProductConfigCommodityLoan(self):
        driver = self.driver
        if self.dict_data["操作类型"] == '新增产品-商品贷':
            self.logstu.info(self.dict_data["操作类型"])
            self.new_Commodity_Config()
        if self.dict_data["操作类型"] == '新增产品失败-商品贷':
            self.logstu.info(self.dict_data["操作类型"])
            self.new_Commodity_Config_fail()
        if self.dict_data["操作类型"] == '修改产品基本信息-商品贷':
            self.logstu.info(self.dict_data["操作类型"])
            self.Commodity_Config_info_modification()
        if self.dict_data["操作类型"] == '产品费用配置移除费用-商品贷':
            self.logstu.info(self.dict_data["操作类型"])
            self.Commodity_Config_remove_cost_modification()
        if self.dict_data["操作类型"] == '产品费用配置导入费用-商品贷':
            self.logstu.info(self.dict_data["操作类型"])
            self.Commodity_Config_Import_cost_modification()
        if self.dict_data["操作类型"] == '产品费用配置导入滞纳金-商品贷':
            self.logstu.info(self.dict_data["操作类型"])
            self.Commodity_Config_Import_surcharge_modification()

    def new_Commodity_Config(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'新增')
        ###进入到新增界面
        time.sleep(2)
        # 输入增新信息
        self.pub.input_values(self.dict_data, 'product', 'right', 'myiframe0')
        # 点击保存按钮
        self.pub.comeinifm('right')
        time.sleep(10)
        self.pub.timeoutBtnClick(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        if u"该产品名称已被占用，请输入新的产品名称" == text:
            self.logstu.info(u"该产品名称已被占用,新增失败")
            # 引发一个断言错误
            #self.assertEqual(1, 2)
        time.sleep(1)
        #获取产品代码
        self.pub.comeinifm('right', 'myiframe0')
        try:
            btn = driver.find_element_by_css_selector("input[name='R0F0']")
            Value = btn.get_attribute("value")
            #self.logstu.info("11111111111111" + Value)
        except Exception as e:
            self.logstu.error(e)
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'], Value, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)

    def new_Commodity_Config_fail(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'新增')
        ###进入到新增界面
        time.sleep(2)
        # 输入增新信息
        self.pub.input_values(self.dict_data, 'product', 'right', 'myiframe0')
        # 点击保存按钮
        self.pub.comeinifm('right')
        #输入信息后点击返回
        self.pub.timeoutBtnClick(u'返回')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        time.sleep(1)

    def Commodity_Config_Import_surcharge_modification(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        # 查看有多少条数据
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'详情')
        time.sleep(1)
        # 进入产品配置界面
        self.pub.comeinifm('ObjectList', 'left')
        self.pub.click_text_btn(u"费用配置", "title")

        hands1 = driver.window_handles
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.thread_btn(u"导入滞纳金")
        text = self.pub.is_alert_and_close_and_get_text()
        if text == u"已经有滞纳金配置，要引入新的滞纳金请先移除现有的滞纳金！！":
            #已经有滞纳金，引入失败，引发一个失败
            self.logstu.debug(text)
            self.assertEqual(1,2)
            return
        self.pub.comeinifm('ObjectList', 'myiframe0')
        self.pub.table_text_clicks(self.dict_data)

        driver.switch_to_default_content()
        self.pub.table_BtnClick2(u'确认')
        self.logstu.debug(self.pub.is_alert_and_close_and_get_text())
        hands2 = driver.window_handles
        for t in range(0, 10):
            if len(hands2) < len(hands1):
                self.logstu.debug(u"原来的窗体：" + hands1.__str__() + u"现有窗体：" + hands2.__str__())
                try:
                    driver.switch_to_window(hands2[-1])
                except Exception as e:
                    self.pub.logstu.debug(e)

        time.sleep(1)

    def Commodity_Config_info_modification(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        # 查看有多少条数据
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'详情')
        time.sleep(1)
        #进入对应标题
        self.pub.comeinifm('ObjectList', 'left')
        self.pub.click_text_btn(u"产品基本信息","title")
        # 修改内容
        self.pub.input_values(self.dict_data, 'product_info', 'ObjectList', 'right', 'myiframe0')
        # 保存按钮
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.thread_btn(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)

    def Commodity_Config_Import_cost_modification(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        # 查看有多少条数据
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'详情')
        time.sleep(1)
        # 进入产品配置界面
        self.pub.comeinifm('ObjectList', 'left')
        self.pub.click_text_btn(u"费用配置","title")

        hands1 = driver.window_handles
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.thread_btn(u"导入费用")
        self.pub.comeinifm('ObjectList', 'myiframe0')
        self.pub.table_text_clicks(self.dict_data)

        driver.switch_to_default_content()
        self.pub.table_BtnClick2(u'确认')
        self.logstu.debug(self.pub.is_alert_and_close_and_get_text())
        hands2 = driver.window_handles
        for t in range(0, 10):
            if len(hands2) < len(hands1):
                self.logstu.debug(u"原来的窗体：" + hands1.__str__() + u"现有窗体：" + hands2.__str__())
                try:
                    driver.switch_to_window(hands2[-1])
                except Exception as e:
                    self.pub.logstu.debug(e)

        time.sleep(1)

    def Commodity_Config_remove_cost_modification(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        # 查看有多少条数据
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.pub.table_RowClick(1)
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.thread_btn(u'详情')
        time.sleep(1)
        # 进入产品配置界面
        self.pub.comeinifm('ObjectList', 'left')
        self.pub.click_text_btn(u"费用配置", "title")

        self.pub.comeinifm('ObjectList', 'right','myiframe0')
        self.pub.table_text_clicks(self.dict_data)
        self.pub.comeinifm('ObjectList', 'right')
        self.pub.thread_btn(u"移除费用")
        self.pub.logstu.debug(self.pub.is_alert_and_close_and_get_text())

        time.sleep(1)
