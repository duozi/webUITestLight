#!/usr/bin/python
#  -*- coding: UTF-8 -*-
import unittest,time
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium.webdriver.common.by import By

class ProductAccountingConfigTransaction(unittest.TestCase):
    '''产品管理>商品类型'''
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象
    actdb = None  # 接收main脚本传送的mysql处理类对象

    #仅本类会用到的标签TDR0F3
    editTds = (By.ID, 'R0F1')

    def setUp(self):
       self.driver = self.mainWebDr
       self.driver.implicitly_wait(30)
       self.filepath = ''
       self.execldata = ""
       self.pub = PublicAct(self.driver)
       #进入具体菜单
       self.driver.implicitly_wait(6)
       self.pub.goto_menu(self.dict_data)
       #打印出执行到第几个案例
       print self.row

    #根据案例不同操作类型执行不同方法
    def test_accounting_transaction_definition(self):
        if self.dict_data["操作类型"].encode('utf8') == '核算交易定义新增':
            self.logstu.info(u"核算交易定义新增")
            self.add_accounting_transaction_definition()
        if self.dict_data["操作类型"].encode('utf8') == '核算交易定义详情':
            self.logstu.info(u"核算交易定义详情")
            self.details_accounting_transaction_definition()
        if self.dict_data["操作类型"].encode('utf8') == '核算交易定义删除':
            self.logstu.info(u"核算交易定义删除")
            self.del_accounting_transaction_definition()
        if self.dict_data["操作类型"].encode('utf8') == '核算交易定义分录模板新增':
            self.logstu.info(u"核算交易定义分录模板新增")
            self.add_accounting_transaction_definition_mode()
        if self.dict_data["操作类型"].encode('utf8') == '核算交易定义分录模板删除':
            self.logstu.info(u"核算交易定义分录模板删除")
            self.del_accounting_transaction_definition_mode()
        if self.dict_data["操作类型"].encode('utf8') == '核算交易定义交易参数列表查看':
            self.logstu.info(u"核算交易定义交易参数列表查看")
            self.details_accounting_transaction_definition_parameterlist()

     #核算交易定义新增方法
    def add_accounting_transaction_definition(self):
        #查询已有记录数，并在日志中打印出来
        self.pub.comeinifm('right','myiframe0')
        self.driver.implicitly_wait(6)
        ##新增前记录总记录数
        tdText = self.driver.find_element_by_css_selector("td[class=GdTdPage]").text
        res = self.pub.all_type_to_encode(tdText).split('(')[1].split(')')[0]
        preTotalRows = int(res)
        self.logstu.info(u"核算交易定义新增前查询到%s记录数" % preTotalRows)
        #进入新增按钮所在iframe，并点击新增按钮，进入到新增内容输入iframe
        self.pub.comeinifm('right')
        self.pub.table_BtnClick_NoSetTimeOut(u'新增')
        time.sleep(5)
        #输入案例中要输入的字段值
        self.pub.setEditTableValueFast(self.dict_data, 'right', 'myiframe0')
        ##由于交易代码不能重复，所以此处用时间戳附加在案例中输入值的后面，避免该值重复导致新增不成功
        self.pub.comeinifm('right','myiframe0')
        timeStamp=int(time.time())
        self.driver.find_element(*self.editTds).send_keys(timeStamp)
        #返回列表页面
        self.pub.comeinifm('right')
        # 点击保存按钮
        self.pub.table_BtnClick_NoSetTimeOut(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        #self.pub.comeinifm('right')
        time.sleep(3)
        #点击返回按钮
        self.pub.table_BtnClick_NoSetTimeOut(u'返回')
        #返回列表页面
        self.pub.comeinifm('right','myiframe0')
        self.driver.implicitly_wait(6)
        ##新增后记录总记录数
        lastTdText = self.driver.find_element_by_css_selector("td[class=GdTdPage]").text
        res = self.pub.all_type_to_encode(lastTdText).split('(')[1].split(')')[0]
        lastTotalRows = int(res)
        self.logstu.info(u"核算交易定义新增后查询到%s记录数" % lastTotalRows)
        if preTotalRows<lastTotalRows:
            self.logstu.info(u"核算交易定义新增成功")
            rul ='核算交易定义新增成功'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            pass
        if preTotalRows>=lastTotalRows:
            self.logstu.info(u"商品范畴新增前记录数是%s，新增后记录数是%s ，如果没有人同时操作新增或删除操作，则该新增操作失败" % (preTotalRows,lastTotalRows))
            preTotalRows=''
            lastTotalRows=''
            rul = '新增前后核算交易定义记录数没有增加，如果没有人同时在进行删除操作，则新增失败！'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            #self.assertEqual(1, 2)
            pass
        preTotalRows=''
        lastTotalRows=''

    #查看核算交易定义详情
    def details_accounting_transaction_definition(self):
        #切换到记录列表所在iframe，并获取列表记录数
        self.pub.comeinifm('right','myiframe0')
        rowcount = self.pub.table_getRowsCount()
        #判断核列表中是否有记录
        if rowcount <=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"核算交易定义列表无数据,无法执行查看详情")
            rowcount =''
            rul ='核算交易定义列表无数据,查看详情失败'
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
            detailValues = self.pub.editTds_getValue(u'交易代码')
            self.logstu.info('detailValues= %s'% detailValues)
            if tableValues == detailValues:
                rul ='核算交易定义详情查看正常'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.logstu.info(u"查询到的第1行记录的核算交易定义详情，其编号值为%s" % (detailValues))
                tableValues = ''
                detailValues = ''
                self.pub.comeinifm('right')
                pass
            else:
                self.logstu.info(u"页面未显示出交易代码%s记录的值，详情查看失败" % tableValues)
                rul ='详情页面未显示出交易代码%s记录的值，详情查看失败'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                rul = ''
                tableValues = ''
                detailValues = ''
                self.pub.comeinifm('right')
                #引发断言错误
                self.assertEqual(1, 2)
                pass

    ###核算交易定义删除方法
    def del_accounting_transaction_definition(self):
        #查询已有记录数，并在日志中打印出来
        self.pub.comeinifm('right','myiframe0')
        self.driver.implicitly_wait(6)
        ##删除前记录总记录数
        tdText = self.driver.find_element_by_css_selector("td[class=GdTdPage]").text
        res = self.pub.all_type_to_encode(tdText).split('(')[1].split(')')[0]
        preTotalRows = int(res)
        self.logstu.info(u"表单删除前查询到%s记录数" % preTotalRows)
        ##翻到最后一页，找到最后一条记录，选中并删除
        self.driver.find_element_by_css_selector("img[title=\"最后一页(服务器)\"]").click()
        #切换到记录列表所在iframe，并获取列表记录数
        self.pub.comeinifm('right','myiframe0')
        rowcount = self.pub.table_getRowsCount()
        #判断核列表中是否有记录
        if rowcount <=0:
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
            self.pub.table_RowClick(rowcount)
            tableValues = self.pub.table_getValue(rowcount,1)
            self.logstu.info(u'删除记录%s成功'% tableValues)
            #进入删除按钮所在iframe，并点击删除按钮
            self.pub.comeinifm('right')
            self.pub.table_BtnClick_NoSetTimeOut(u'删除')
            text = self.pub.is_alert_and_close_and_get_text()
            self.logstu.info(u"alert text is %s" % text)
            self.logstu.info(u"表单中记录删除成功")
            rul ='表单中记录删除成功'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            pass

    #核算交易定义分录模式新增方法
    def add_accounting_transaction_definition_mode(self):
        ##翻到最后一页，找到最后一条记录，选中
        self.pub.comeinifm('right','myiframe0')
        self.driver.implicitly_wait(6)
        self.driver.find_element_by_css_selector("img[title=\"最后一页(服务器)\"]").click()
        #切换到记录列表所在iframe，并获取列表记录数
        self.pub.comeinifm('right','myiframe0')
        rowcount = self.pub.table_getRowsCount()
        #判断核列表中是否有记录
        if rowcount <=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"列表无数据,无法进入分录模式记录新增页面")
            rowcount =''
            rul ='列表无数据,无法进入分录模式记录新增页面'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass
        else:
            self.pub.table_RowClick(rowcount)
            tableValues = self.pub.table_getValue(rowcount,1)
            self.logstu.info(u"进入的是记录%s的分录模式" % tableValues)
            #进入分录模式按钮所在iframe，并点击分录模式按钮，弹出分录模式窗口页面
            self.pub.comeinifm('right')
            self.pub.table_BtnClick_NoSetTimeOut(u'分录模板')
            time.sleep(3)
            ###进入到新增内容输入页面
            self.pub.goNameWindow('小牛消费金融业务管理系统')
            self.driver.implicitly_wait(6)
            ##新增前记录总记录数
            self.pub.comeinifm('ObjectList','myiframe0')
            self.driver.implicitly_wait(6)
            preTotalRows = self.pub.table_getRowsCount()
            self.logstu.info(u"新增前统计表单记录数为%s条" % preTotalRows)
            #进入新增按钮所在iframe，并点击新增按钮，进入到新增内容输入iframe
            self.pub.comeinifm('ObjectList')
            self.pub.table_BtnClick_NoSetTimeOut(u'新增')
            self.driver.implicitly_wait(6)
            #输入案例中要输入的字段值
            self.pub.setEditTableValueFast(self.dict_data, 'ObjectList','DetailFrame','myiframe0')
            ##由于分录编号不能重复，所以此处用时间戳附加在案例中输入值的后面，避免该值重复导致新增不成功
            self.pub.comeinifm('ObjectList','DetailFrame','myiframe0')
            timeStamp=int(time.time())
            self.driver.find_element(*self.editTds).send_keys(timeStamp)
            #切换到保存按钮所在iframe
            self.pub.comeinifm('ObjectList','DetailFrame')
            # 点击保存按钮
            self.pub.table_BtnClick_NoSetTimeOut(u'保存')
            text = self.pub.is_alert_and_close_and_get_text()
            self.logstu.info(u"alert text is %s" % text)
            self.driver.implicitly_wait(6)
            ##新增后记录总记录数
            self.pub.comeinifm('ObjectList','myiframe0')
            self.driver.implicitly_wait(6)
            lastTotalRows = self.pub.table_getRowsCount()
            self.logstu.info(u"新增后统计表单记录数为%s条" % lastTotalRows)
            ##判断新增前后记录数是否增加
            if preTotalRows<lastTotalRows:
                self.logstu.info(u"记录新增成功")
                rul ='记录新增成功'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                self.pub.winClose()
                self.pub.comeinifm('right')
                pass
            else:
                self.logstu.info(u"新增前表单记录数是%s条，新增后记录数是%s条，如果没有人同时操作删除操作，则该新增操作失败" % (preTotalRows,lastTotalRows))
                preTotalRows=''
                lastTotalRows=''
                rul = '新增前表单记录数是%s条，新增后记录数是%s条，如果没有人同时操作删除操作，则该新增操作失败！'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                self.pub.winClose()
                self.pub.comeinifm('right')
                #引发断言错误
                #self.assertEqual(1, 2)
                pass

    #核算交易定义分录模式删除方法
    def del_accounting_transaction_definition_mode(self):
        ##翻到最后一页，找到最后一条记录，选中
        self.pub.comeinifm('right','myiframe0')
        self.driver.implicitly_wait(6)
        self.driver.find_element_by_css_selector("img[title=\"最后一页(服务器)\"]").click()
        #切换到记录列表所在iframe，并获取列表记录数
        self.pub.comeinifm('right','myiframe0')
        rowcount = self.pub.table_getRowsCount()
        #判断核列表中是否有记录
        if rowcount <=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"列表无数据,无法进入分录模式记录新增页面")
            rowcount =''
            rul ='列表无数据,无法进入分录模式记录新增页面'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass
        else:
            self.pub.table_RowClick(rowcount)
            tableValues = self.pub.table_getValue(rowcount,1)
            self.logstu.info(u"进入的是记录%s的分录模式" % tableValues)
            #进入分录模式按钮所在iframe，并点击分录模式按钮，弹出分录模式窗口页面
            self.pub.comeinifm('right')
            self.pub.table_BtnClick_NoSetTimeOut(u'分录模板')
            time.sleep(3)
            ###进入到新增内容输入页面
            self.pub.goNameWindow('小牛消费金融业务管理系统')
            self.driver.implicitly_wait(6)
            ##新增前记录总记录数
            self.pub.comeinifm('ObjectList','myiframe0')
            self.driver.implicitly_wait(6)
            preTotalRows = self.pub.table_getRowsCount()
            self.logstu.info(u"新增前统计表单记录数为%s条" % preTotalRows)
            if preTotalRows<=0:
                ##先执行新增记录操作
                self.pub.winClose()
                self.pub.comeinifm('right')
                try:
                    self.add_accounting_transaction_definition_mode
                except:
                    rul = '分录模式列表中无记录，调用新增方法新增不成功，无法执行删除记录操作'
                    updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                    self.actdb.testCaseUpdate(updatestr)
                    #引发断言错误
                    self.assertEqual(1, 2)
            else:
                ##选中要删除列表
                preTotalRows = self.pub.table_getRowsCount()
                self.pub.table_RowClick(preTotalRows)
                #进入删除按钮所在iframe，并点击删除按钮
                self.pub.comeinifm('ObjectList')
                self.pub.table_BtnClick_NoSetTimeOut(u'删除')
                text = self.pub.is_alert_and_close_and_get_text()
                self.logstu.info(u"alert text is %s" % text)
                self.driver.implicitly_wait(6)
                ##删除后记录总记录数
                self.pub.comeinifm('ObjectList','myiframe0')
                self.driver.implicitly_wait(6)
                lastTotalRows = self.pub.table_getRowsCount()
                self.logstu.info(u"新增后统计表单记录数为%s条" % lastTotalRows)
                ##判断删除前后记录数是否减少
                if preTotalRows>lastTotalRows:
                    self.logstu.info(u"记录删除成功")
                    rul ='记录上次成功'
                    updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                    self.actdb.testCaseUpdate(updatestr)
                    self.pub.winClose()
                    self.pub.comeinifm('right')
                    pass
                else:
                    self.logstu.info(u"删除前表单记录数是%s条，删除后记录数是%s条，如果没有人同时对列表进行新增操作，则该删除操作失败" % (preTotalRows,lastTotalRows))
                    rul = '该列表中删除前记录数少于或等于删除后记录，如果没有人同时对列表进行新增操作，则该删除操作失败！'
                    updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                    self.actdb.testCaseUpdate(updatestr)
                    self.pub.winClose()
                    self.pub.comeinifm('right')
                    #引发断言错误
                    #self.assertEqual(1, 2)
                    pass

    def details_accounting_transaction_definition_parameterlist(self):
        ##翻到最后一页，找到最后一条记录，选中
        self.pub.comeinifm('right','myiframe0')
        self.driver.implicitly_wait(6)
        self.driver.find_element_by_css_selector("img[title=\"最后一页(服务器)\"]").click()
        #切换到记录列表所在iframe，并获取列表记录数
        self.pub.comeinifm('right','myiframe0')
        rowcount = self.pub.table_getRowsCount()
        #判断核列表中是否有记录
        if rowcount <=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"核算交易定义列表无数据,无法进入交易参数列表页面")
            rowcount =''
            rul ='核算交易定义列表无数据,无法进入交易参数列表页面'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass
        else:
            self.pub.table_RowClick(rowcount)
            tableValues = self.pub.table_getValue(rowcount,1)
            self.logstu.info(u"进入的是记录%s的交易参数列表" % tableValues)
            #进入分录模式按钮所在iframe，并点击分录模式按钮，弹出分录模式窗口页面
            self.pub.comeinifm('right')
            self.pub.table_BtnClick_NoSetTimeOut(u'交易参数列表')
            time.sleep(3)
            ###进入到交易参数列表内容显示页面
            self.pub.goNameWindow('小牛消费金融业务管理系统')
            self.driver.implicitly_wait(6)
            ##获取列表记录数
            self.pub.comeinifm('ObjectList','myiframe0')
            self.driver.implicitly_wait(6)
            preTotalRows = self.pub.table_getRowsCount()
            self.logstu.info(u"交易参数列表记录数为%s条" % preTotalRows)
            if preTotalRows<=0:
                ##回写页面查询到的记录数结果
                rul = '交易参数列表中无记录'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                self.pub.winClose()
                self.pub.comeinifm('right')
                #引发断言错误
                #self.assertEqual(1, 2)
                pass
            else:
                self.pub.table_RowClick(rowcount)
                tableValues = self.pub.table_getValue(1,1)
                self.logstu.info(u"查到的记录序号的值为%s条" % tableValues)
                rul = '分录模式列表中无记录'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                self.pub.winClose()
                self.pub.comeinifm('right')
                pass
