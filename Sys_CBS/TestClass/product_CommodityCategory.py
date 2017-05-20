#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
from script.testunite.comm.commFunction import CommFunction
from script.testunite.comm.lyElementsOperation import PublicAct

class ProductCommodityCategory(unittest.TestCase):
    #产品管理-商品类型：增删改查
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数

    def setUp(self):
        self.driver = self.mainWebDr
        #self.comm = CommFunction()
        self.pub = PublicAct(self.driver)

        #self.mainWebDr = self.pub.autoLogin()
        print 'self.mainWebDr:'
        print self.mainWebDr
        print 'self.driver:'
        print self.driver
        print 'run row:'
        print self.row
        # 进入具体菜单项
        #self.comm.goto_menu(self.driver, self.row)
        self.pub.goto_menu(self.dict_data)

    def test_productAct(self):
        driver = self.driver

        if self.pub.all_type_to_encode(self.dict_data["操作类型"]) == '查询':
            self.pub.comeinifm('right', 'rightup')
            self.pub.select_sets(self.dict_data)
            self.pub.select_btn(u'查询')
            driver.switch_to_default_content()

        # 修改详情页数据并保存
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]) == '详情修改':
            # 首先利用查询条件确认要修改的数据，用查询结果的第一条数据测试
            self.pub.comeinifm('right', 'rightup')
            self.pub.select_sets(self.dict_data)
            self.pub.select_btn(u'查询')
            driver.switch_to_default_content()
            # 点击查询结果第一条数据
            self.pub.comeinifm('right', 'rightup', 'myiframe0')
            self.pub.table_RowClick(1)
            driver.switch_to_default_content()
            # 打开详情页面
            self.pub.comeinifm('right', 'rightup')
            self.pub.thread_btn(u'详情')
            driver.switch_to_default_content()

            # 编辑详情页，最后按下保存和返回
            self.pub.setEditTableValues(self.dict_data, 'right', 'rightup', 'myiframe0')
            self.pub.comeinifm('right', 'rightup')
            self.pub.thread_btn(u'保存')
            self.pub.thread_btn(u'返回')
            driver.switch_to_default_content()

        # 预期结果对比
        print '预期结果: ' + self.pub.all_type_to_encode(self.dict_data["预期结果"])
        self.pub.comeinifm('right', 'rightup')
        self.pub.select_sets(self.dict_data)
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()
        sel_text = self.pub.all_type_to_encode(self.dict_data['预期结果'])
        self.pub.comeinifm('right', 'rightup', 'myiframe0')
        checkValue = self.pub.table_getValue2(1, sel_text.split('|')[0])
        driver.switch_to_default_content()
        self.assertEqual(self.pub.all_type_to_encode(sel_text.split('|')[1]), checkValue)


if __name__ == "__main__":
    unittest.main()