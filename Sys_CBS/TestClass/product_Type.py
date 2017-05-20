#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest,time
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium.webdriver.common.by import By

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class ProductType(unittest.TestCase):
    '''产品管理>商品类型'''
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象
    actdb = None  # 接收main脚本传送的mysql处理类对象

    #仅本类会用到的标签TDR0F3
    editTds = (By.ID, 'R0F3')
    #editTds = (By.CSS_SELECTOR, 'table#dztable >tbody >tr >td'

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
    def test_product_type(self):
        if self.dict_data["操作类型"].encode('utf8') == '商品范畴新增':
            self.logstu.info(u"商品范畴新增")
            self.add_product_category()
        if self.dict_data["操作类型"].encode('utf8') == '商品范畴详情':
            self.logstu.info(u"商品范畴详情")
            self.details_product_category()
        if self.dict_data["操作类型"].encode('utf8') == '商品范畴查询':
            self.logstu.info(u"商品范畴查询")
            self.query_product_category()
        if self.dict_data["操作类型"].encode('utf8') == '商品类型新增':
            self.logstu.info(u"商品类型新增")
            self.add_product_type()
        if self.dict_data["操作类型"].encode('utf8') == '商品类型详情':
            self.logstu.info(u"商品类型详情")
            self.details_product_type()

    #新增商品范畴方法
    def add_product_category(self):
        #查询已有记录数，并在日志中打印出来
        self.pub.comeinifm('right','rightup','myiframe0')
        prerowcount = self.pub.table_getRowsCount()
        self.logstu.info(u"商品范畴新增前查询到%s记录数" % prerowcount)
        #进入新增按钮所在iframe，并点击新增按钮
        self.pub.comeinifm('right','rightup')
        self.pub.table_BtnClick_NoSetTimeOut(u'新增')
        ###进入到新增内容输入页面
        self.pub.goNameWindow('小牛消费金融业务管理系统')
        time.sleep(5)
        #输入案例中要输入的字段值
        self.pub.setEditTableValueFast(self.dict_data, 'ObjectList', 'myiframe0')
        ###由于范畴编码不能重复，所以此处用时间戳附加在案例中输入值的后面，避免该值重复导致新增不成功
        self.pub.comeinifm('ObjectList','myiframe0')
        timeStamp=int(time.time())
        self.driver.find_element(*self.editTds).send_keys(timeStamp)
        #返回列表页面
        self.pub.comeinifm('ObjectList')
        # 点击保存按钮
        self.pub.table_BtnClick_NoSetTimeOut(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        self.pub.winClose()
        #判断是否新增成功
        self.pub.comeinifm('right')
        self.pub.comeinifm('right','rightup','myiframe0')
        lastrowcount = self.pub.table_getRowsCount()
        self.logstu.info(u"商品范畴新增后查询到%s记录数" % lastrowcount)
        if prerowcount<lastrowcount:
            self.logstu.info(u"商品范畴新增成功")
            rul = '商品范畴新增成功'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            pass
        if prerowcount>=lastrowcount:
            self.logstu.info(u"商品范畴新增前记录数是%s，新增后记录数是%s ，如果没有人同时操作新增或删除操作，则该新增操作失败" % (prerowcount,lastrowcount))
            prerowcount=''
            lastrowcount=''
            rul = '新增前后商品范畴记录数没有增加，如果没有人同时在进行删除操作，则新增失败！'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass
        prerowcount=''
        lastrowcount=''


    def query_product_category(self):
        self.pub.comeinifm('right','rightup')
        #输入查询参数，执行查询
        self.pub.selectAutoSets(self.dict_data)
        #进入查询记录表单所在iframe
        self.pub.comeinifm('right','rightup','myiframe0')
        #统计查询结果记录数
        rowcount = self.pub.table_getRowsCount()
        #判断查询结果
        if rowcount>0:
            self.logstu.info(u"商品范畴查询执行成功，查询到%s记录数" % rowcount)
            rowcount=''
            pass
        if rowcount == 0:
            self.logstu.info(u"商品范畴查询执行完成，但是查询到的记录数是%s条" % rowcount)
            rowcount=''
        #返回商品类型页面
        self.pub.comeinifm('right')

    #查看商品范畴详情
    def details_product_category(self):
        #初始化商品范畴记录数
        rowcount = 0
        #切换到商品范畴列表所在iframe，并获取列表记录数
        self.pub.comeinifm('right','rightup','myiframe0')
        rowcount = self.pub.table_getRowsCount()
        #判断商品范畴列表中是否有记录
        if rowcount <=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"商品范畴列表无数据,无法执行查看商品范畴详情")
            rowcount =''
            rul ='商品范畴列表无数据,查看详情失败'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass
        else:
            #有商品范畴记录执行该部分代码
            self.logstu.info(u"列表中包含%s条商品范畴"%rowcount)
            k = 0
            i = 0
            #循环查找看哪条商品范畴记录有商品类型记录
            for i in range(1,rowcount):
                self.pub.table_RowClick(i)
                upValues=self.pub.table_getValue(i,1)
                self.pub.comeinifm('right')
                self.pub.comeinifm('right','rightdown','myiframe0')
                lasdowntablerow = self.pub.table_getRowsCount()
                if lasdowntablerow>=0:
                    k = i
                    break
                else:
                    self.pub.comeinifm('right')
                    self.pub.comeinifm('right','rightup','myiframe0')
                    lasdowntablerow=''
                    upValues=''
                    continue
            if k==0:
                self.logstu.info(u"该商品范畴下的无商品详情列表记录数")
                rul ='该商品范畴下的无商品详情列表记录数，查看详情不成功'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                rul=''
                k=''
                self.pub.comeinifm('right')
                #引发断言错误
                self.assertEqual(1, 2)
                pass
            else:
                rul ='商品范畴详情查看正常'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.logstu.info(u"该商品范畴下的商品详情列表记录数为%s条" % lasdowntablerow)
                downValues = self.pub.table_getValue(1,1)
                self.logstu.info(u"第%s行记录商品范畴编号值为%s，该记录详情的第1行记录的商品类型编号值为%s条" % (k,upValues,downValues))
                k=''
                upValues=''
                downValues=''
                self.pub.comeinifm('right')
                pass

    #新增商品类型
    def add_product_type(self):
        #查询已有记录数，并在日志中打印出来
        self.pub.comeinifm('right','rightup','myiframe0')
        uprowcount = self.pub.table_getRowsCount()
        if uprowcount<=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"商品范畴列表无数据,无法执行查看商品类型新增操作")
            uprowcount =''
            rul ='商品范畴列表无数据,无法显示商品类型新增按钮,商品类型新增失败'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            rul = ''
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass
        else:
            self.logstu.info(u"商品范畴列表有%s记录数" % uprowcount)
            self.pub.table_RowClick(1)
            upValues=self.pub.table_getValue(1,1)
            #进入商品类型新增按钮所在iframe，并点击新增按钮
            self.pub.comeinifm('right','rightdown','myiframe0')
            predowntablerow = self.pub.table_getRowsCount()
            self.logstu.info(u"商品类型新增前查询到%s记录数" % predowntablerow)
            #进入新增按钮所在iframe，并点击新增按钮
            self.pub.comeinifm('right','rightdown')
            self.pub.table_BtnClick_NoSetTimeOut(u'新增')
            time.sleep(5)
            #进入到新增内容输入页面,输入案例中要输入的字段值
            self.pub.setEditTableValueFast(self.dict_data,'right','rightdown','myiframe0')
            #切换到rightdown的iframe
            self.pub.comeinifm('right','rightdown')
            # 点击保存按钮
            self.pub.table_BtnClick_NoSetTimeOut(u'保存')
            text = self.pub.is_alert_and_close_and_get_text()
            self.logstu.info(u"alert text is %s" % text)
            #点击返回按钮，返回列表页面
            self.pub.table_BtnClick_NoSetTimeOut(u'返回')
            #判断是否新增成功
            self.pub.comeinifm('right','rightdown','myiframe0')
            lastdownrowcount = self.pub.table_getRowsCount()
            self.logstu.info(u"商品类型新增后查询到%s记录数" % lastdownrowcount)
            if predowntablerow<lastdownrowcount:
                self.logstu.info(u"商品类型新增成功")
                self.pub.comeinifm('right')
                pass
            if predowntablerow>=lastdownrowcount:
                self.logstu.info(u"商品范畴新增前记录数是%s，新增后记录数是%s ，如果没有人同时操作新增或删除操作，则该新增操作失败" % (predowntablerow,lastdownrowcount))
                predowntablerow=''
                lastdownrowcount=''
                rul = '新增前后商品范畴记录数没有增加，如果没有人同时在进行删除操作，则新增失败！'
                rul ='商品范畴列表无数据,查看详情失败'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                self.pub.comeinifm('right')
                #引发断言错误
                self.assertEqual(1, 2)
                pass
            predowntablerow=''
            lastdownrowcount=''

    #查看商品类型详情
    def details_product_type(self):
        #切换到商品范畴列表所在iframe，并获取列表记录数
        self.pub.comeinifm('right','rightup','myiframe0')
        rowcount = self.pub.table_getRowsCount()
        #判断商品范畴列表中是否有记录
        if rowcount <=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"商品范畴列表无数据,无法执行查看商品类型详情")
            rowcount =''
            rul ='商品范畴列表无数据,查看商品类型详情失败'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
            pass
        else:
            #有商品范畴记录执行该部分代码
            self.logstu.info(u"列表中包含%s条商品范畴记录"%rowcount)
            k = 0
            #循环查找看哪条商品范畴记录有商品类型记录
            for i in range(1,rowcount):
                self.pub.table_RowClick(i)
                upValues=self.pub.table_getValue(i,1)
                #self.pub.comeinifm('right')
                self.pub.comeinifm('right','rightdown','myiframe0')
                lasdowntablerow = self.pub.table_getRowsCount()
                if lasdowntablerow>=0:
                    k = i
                    break
                else:
                    self.pub.comeinifm('right')
                    self.pub.comeinifm('right','rightup','myiframe0')
                    lasdowntablerow=''
                    upValues=''
                    continue
            if k==0:
                self.logstu.info(u"所有商品范畴下商品类型列表都无记录数，商品类型详情查看失败")
                rul ='所有商品范畴下商品类型列表都无记录数，商品类型详情查看失败'
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                rul=''
                k=''
                self.pub.comeinifm('right')
                #引发断言错误
                self.assertEqual(1, 2)
                pass
            else:
                self.pub.table_RowClick(1)
                downValues = self.pub.table_getValue(1,1)
                self.pub.comeinifm('right','rightdown')
                self.pub.table_BtnClick(u'详情')
                self.pub.comeinifm('right','rightdown','myiframe0')
                self.driver.implicitly_wait(10)
                detailValues = self.pub.editTds_getValue(u'商品类型编号')
                self.logstu.info('detailValues= %s'% detailValues)
                if downValues == detailValues:
                    rul ='商品类型详情查看正常'
                    updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                    self.logstu.info(u"查询到的是第%s行记录商品范畴编号值为%s的记录下的第1行记录的商品类型详情，其编号值为%s" % (k,upValues,downValues))
                    k = ''
                    upValues = ''
                    downValues = ''
                    detailValues = ''
                    self.pub.comeinifm('right')
                    pass
                else:
                    self.logstu.info(u"页面未显示出商品类型编号%s记录的值，商品类型详情查看失败" % downValues)
                    rul ='页面未显示出商品类型编号%s记录的值，商品类型详情查看失败'
                    updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                    self.actdb.testCaseUpdate(updatestr)
                    rul = ''
                    k = ''
                    downValues = ''
                    detailValues = ''
                    self.pub.comeinifm('right')
                    #引发断言错误
                    self.assertEqual(1, 2)
                    pass





