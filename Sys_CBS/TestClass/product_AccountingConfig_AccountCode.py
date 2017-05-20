#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest,time
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium.webdriver.common.by import By


class ProductAccountingConfigAccountCode(unittest.TestCase):
    '''产品管理>核算参数定义>财务代码定义'''
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象
    actdb = None  # 接收main脚本传送的mysql处理类对象

    #仅本类会用到的标签TDR0F3
    editTds = (By.ID, 'R0F1')
    alinksId = (By.ID, 'text1')

    def setUp(self):
       self.driver = self.mainWebDr
       self.driver.implicitly_wait(30)
       self.filepath = ''
       self.execldata = ""
       self.pub = PublicAct(self.driver)
       self.logstu.info(self.pub.all_type_to_encode(self.dict_data["案例名称"]) + '---' + self.pub.all_type_to_encode(
            self.dict_data["案例详情"]))
       #进入具体菜单
       self.driver.implicitly_wait(6)
       self.pub.goto_menu(self.dict_data)
       #进入左边菜单
       self.pub.leftMenuVagueClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[0], 'left')
       #打印出执行到第几个案例
       print self.row

    #根据案例不同操作类型执行不同方法
    def test_Product_AccountingConfig_AccountCode(self):
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '新增':
            self.logstu.info(u"财务代码定义新增")
            self.add_Product_AccountingConfig_AccountCode()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '查询':
            self.logstu.info(u"财务代码定义查询")
            self.query_Product_AccountingConfig_AccountCode()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '详情':
            self.logstu.info(u"财务代码定义详情")
            self.details_Product_AccountingConfig_AccountCode()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '删除':
            self.logstu.info(u"财务代码定义删除")
            self.del_Product_AccountingConfig_AccountCode()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '财务方案新增':
            self.logstu.info(u"财务方案新增")
            self.add_Accounting_Scheme()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] == '账务代码新增':
            self.logstu.info(u"账务代码新增")
            # self.add_Accounting_Code()

    #财务代码定义 新增
    def add_Product_AccountingConfig_AccountCode(self):
        #查询已有记录数，并在日志中打印出来
        self.pub.comeinifm('right','myiframe0')
        prerowcount = self.pub.table_getRowsCount()
        self.logstu.info(u"新增前记录总数为%s条" % prerowcount)
        #进入新增按钮所在iframe，并点击新增按钮
        self.pub.comeinifm('right')
        self.pub.table_BtnClick_NoSetTimeOut(u'新增')
        ###进入到新增内容输入页面
        #输入案例中要输入的字段值
        self.pub.setEditTableValueFast(self.dict_data, 'right', 'myiframe0')
        ###由于范畴编码不能重复，所以此处用时间戳附加在案例中输入值的后面，避免该值重复导致新增不成功
        self.pub.comeinifm('right','myiframe0')
        timeStamp=int(time.time())
        self.driver.find_element(*self.editTds).send_keys(timeStamp)
        #返回列表页面
        self.pub.comeinifm('right')
        # 点击保存按钮
        self.pub.table_BtnClick_NoSetTimeOut(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        #点击返回按钮
        self.pub.table_BtnClick_NoSetTimeOut(u'返回')
        #判断是否新增成功
        self.pub.comeinifm('right','myiframe0')
        lastrowcount = self.pub.table_getRowsCount()
        self.logstu.info(u"新增后记录总数为%s条" % lastrowcount)
        if prerowcount<lastrowcount:
            self.logstu.info(u"新增成功")
            rul = '新增成功'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            pass
        if prerowcount>=lastrowcount:
            self.logstu.info(u"新增前记录总数是%s，新增后记录总数是%s ，如果没有人同时操作删除操作，则该新增操作失败" % (prerowcount,lastrowcount))
            rul = '新增前后记录总数没有增加，如果没有人同时在进行删除操作，则新增失败！'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass

    #条件查询
    def query_Product_AccountingConfig_AccountCode(self):
        #进入查询及其输入iframe
        self.pub.comeinifm('right')
        #输入查询参数，执行查询
        self.pub.selectAutoSets(self.dict_data)
        #进入查询记录表单所在iframe
        self.pub.comeinifm('right','myiframe0')
        #统计查询结果记录数
        rowcount = self.pub.table_getRowsCount()
        #判断查询结果
        if rowcount>0:
            self.logstu.info(u"查询执行成功，查询到%s记录数" % rowcount)
            rul = '查询执行成功，查询到%s条记录数！'% rowcount
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            pass
        if rowcount == 0:
            self.logstu.info(u"查询执行完成，但是未查询到任何符合条件的记录" % rowcount)
        #返回商品类型页面
        self.pub.comeinifm('right')

    #查看详情
    def details_Product_AccountingConfig_AccountCode(self):
        #切换到记录列表所在iframe，并获取列表记录数
        self.pub.comeinifm('right','myiframe0')
        rowcount = self.pub.table_getRowsCount()
        #判断核列表中是否有记录
        if rowcount <=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"列表无数据,无法执行查看详情")
            rowcount =''
            rul ='列表无数据,查看详情失败'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass
        else:
            self.pub.table_RowClick(1)
            tableValues = self.pub.table_getValue(1,1)
            self.pub.comeinifm('right')
            self.pub.table_BtnClick(u'详情')
            self.pub.comeinifm('right','myiframe0')
            self.driver.implicitly_wait(10)
            detailValues = self.pub.editTds_getValue(u'科目号')
            self.logstu.info('detailValues= %s'% detailValues)
            if tableValues == detailValues:
                rul ='详情查看正常'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.logstu.info(u"查询到的第1行记录的详情，其科目号值为%s" % (detailValues))
                self.pub.comeinifm('right')
                pass
            else:
                self.logstu.info(u"详情页面未显示出交科目号%s的值，详情查看失败" % tableValues)
                rul ='详情页面未显示出交科目号%s的值，详情查看失败'% tableValues
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                self.pub.comeinifm('right')
                #引发断言错误
                self.assertEqual(1, 2)
                pass

    def del_Product_AccountingConfig_AccountCode(self):
        #查询已有记录数，并在日志中打印出来
        self.pub.comeinifm('right','myiframe0')
        self.driver.implicitly_wait(6)
        ##删除前记录总记录数
        preTotalRows = self.pub.table_getRowsCount()
        self.logstu.info(u"表单删除前查询到%s记录数" % preTotalRows)
        #判断核列表中是否有记录
        if preTotalRows <=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"列表无数据,无法执行删除记录操作")
            rowcount =''
            rul ='列表无数据,无法执行删除记录操作'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass
        else:
            self.pub.table_RowClick(preTotalRows)
            tableValues = self.pub.table_getValue(preTotalRows,1)
            self.logstu.info(u'删除记录%s成功'% tableValues)
            #进入删除按钮所在iframe，并点击删除按钮
            self.pub.comeinifm('right')
            self.pub.table_BtnClick_NoSetTimeOut(u'删除')
            self.logstu.info(u"表单中记录删除成功")
            rul ='表单中记录删除成功'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            #self.pub.comeinifm('right')
            pass

    #LAS科目代码-银行内部账务代码_财务方案新增方法
    def add_Accounting_Scheme(self):
        #查询已有记录数，并在日志中打印出来
        self.pub.comeinifm('right','myiframe0')
        prerowcount = self.pub.table_getRowsCount()
        self.logstu.info(u"新增前记录总数为%s条" % prerowcount)
        #进入新增按钮所在iframe，并点击新增按钮
        self.pub.comeinifm('right')
        self.pub.table_BtnClick_NoSetTimeOut(u'新增')
        ###进入到新增内容输入页面
        self.pub.comeinifm('right','myiframe0')
        #输入案例中要输入的字段值
        self.pub.setTableCellValueFast(self.dict_data,prerowcount+1, 'right', 'myiframe0')
        #返回保存按钮所在iframe
        self.pub.comeinifm('right')
        # 点击保存按钮
        self.pub.table_BtnClick_NoSetTimeOut(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        #判断是否新增成功
        self.pub.comeinifm('right','myiframe0')
        lastrowcount = self.pub.table_getRowsCount()
        self.logstu.info(u"新增后记录总数为%s条" % lastrowcount)
        if prerowcount<lastrowcount:
            self.logstu.info(u"新增成功")
            rul = '新增成功'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            pass
        if prerowcount>=lastrowcount:
            self.logstu.info(u"新增前记录总数是%s，新增后记录总数是%s ，如果没有人同时操作删除操作，则该新增操作失败" % (prerowcount,lastrowcount))
            rul = '新增前后记录总数没有增加，如果没有人同时在进行删除操作，则新增失败！'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass

    #财务代码新增
    # def add_Accounting_Code(self):
    #     #查询已有记录数，并在日志中打印出来
    #     self.pub.comeinifm('right','myiframe0')
    #     rowcount = self.pub.table_getRowsCount()
    #     if rowcount<=0:
    #         #列表无记录数执行该部分代码
    #         self.logstu.info(u"财务方案列表无记录,无法执行财务代码新增操作")
    #         rul ='财务方案列表无记录,无法执行财务代码新增操作,新增失败'
    #         updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
    #         self.actdb.testCaseUpdate(updatestr)
    #         self.pub.comeinifm('right')
    #         #引发断言错误
    #         self.assertEqual(1, 2)
    #         pass
    #     else:
    #         self.logstu.info(u"财务方案列表有%s记录数" % rowcount)
    #         self.pub.table_RowClick(rowcount)
    #         upValues=self.pub.table_getValue(rowcount,1)
    #         #进入商品类型新增按钮所在iframe，并点击新增按钮
    #         self.pub.comeinifm('right','DetailFrame','myiframe0')
    #         pretablerow = self.pub.table_getRowsCount()
    #         self.logstu.info(u"新增前列表有%s记条录数" % pretablerow)
    #         #进入新增按钮所在iframe，并点击新增按钮
    #         self.pub.comeinifm('right','DetailFrame')
    #         self.pub.table_BtnClick_NoSetTimeOut(u'新增')
    #         time.sleep(5)
    #         #进入到新增内容输入页面,输入案例中要输入的字段值
    #         #self.pub.setEditTableValueFast(self.dict_data,'right','DetailFrame','myiframe0')
    #         self.pub.comeinifm('right','DetailFrame','myiframe0')
    #         tdvalue = '贷款正常本金'
    #         self.logstu.info(tdvalue)
    #         # inputTds = (By.ID, 'TDR0F1') #R0F1
    #         # editinput = self.driver.find_elements_by_id('TDR0F1')
    #         selectList1 = (By.CSS_SELECTOR, 'form >div#tableContainer >table >tbody >tr')
    #         # #editinput = self.driver.find_elements(*self.selectList1)
    #         # #self.logstu.info('editinput.tag_name=%s'%editinput.tag_name)
    #         inputtag = self.driver.find_element_by_css_selector('input[name=\"btnR0F1\"]')
    #         tagValue = inputtag.get_attribute("name")
    #         edittr =  self.driver.find_elements(*self.selectList1)
    #         select = edittr.find_element_by_tag_name('select')
    #         allOptions = select.find_elements_by_tag_name("option")
    #         allOptions[1].click()
    #         # self.logstu.info('name=%s'% tagValue)
    #         # if editinput.tag_name == 'select':
    #         #     allOptions = editinput.find_elements_by_tag_name("option")
    #         #     for v in allOptions:
    #         #         if self.all_type_to_encode(v.text) == self.pub.all_type_to_encode(tdvalue):
    #         #             self.logstu.info('v.text='% v.text )
    #         #             v.click()
    #         #             break
    #         #self.pub.setTableCellValueFast(self.dict_data,pretablerow+1, 'right','DetailFrame','myiframe0')
    #         #切换到rightdown的iframe
    #         self.pub.comeinifm('right','DetailFrame')
    #         # 点击保存按钮
    #         self.pub.table_BtnClick_NoSetTimeOut(u'保存')
    #         text = self.pub.is_alert_and_close_and_get_text()
    #         self.logstu.info(u"alert text is %s" % text)
    #         #点击返回按钮，返回列表页面
    #         #self.pub.table_BtnClick_NoSetTimeOut(u'返回')
    #         #判断是否新增成功
    #         self.pub.comeinifm('right','DetailFrame','myiframe0')
    #         lastrowcount = self.pub.table_getRowsCount()
    #         self.logstu.info(u"新增后列表有%s条记录数" % lastrowcount)
    #         if pretablerow<lastrowcount:
    #             self.logstu.info(u"新增成功")
    #             self.pub.comeinifm('right')
    #             pass
    #         if pretablerow>=lastrowcount:
    #             self.logstu.info(u"新增前记录数是%s，新增后记录数是%s ，如果没有人同时操作删除操作，则该新增操作失败" % (pretablerow,lastrowcount))
    #             rul = '新增前后列表记录数没有增加，如果没有人同时在进行删除操作，则新增失败！'
    #             updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
    #             self.actdb.testCaseUpdate(updatestr)
    #             self.pub.comeinifm('right')
    #             #引发断言错误
    #             self.assertEqual(1, 2)
    #             pass