#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest
from Sys_CBS.PageObj.lyElementsOperation import PublicAct

class ProductImageTypeConfig(unittest.TestCase):
    ''' 产品管理>影像文件配置 '''
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象
    actdb = None  # 接收main脚本传送的mysql处理类对象

    #仅本类会用到的标签

    def setUp(self):
        self.driver = self.mainWebDr
        self.driver.implicitly_wait(30)
        self.filepath = ''
        self.execldata = ""
        self.pub = PublicAct(self.driver)
        #打印出执行到第几个案例
        print self.row
        self.logstu.info(self.pub.all_type_to_encode(self.dict_data["案例名称"]) + '---' + self.pub.all_type_to_encode(
            self.dict_data["案例详情"]))
        #进入具体菜单
        self.driver.implicitly_wait(6)
        self.pub.goto_menu(self.dict_data)
        #进入左边菜单
        self.pub.leftMenuVagueClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[0], 'left')
        self.pub.leftMenuVagueClick(self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[1] ,'right','frameleft','left')

    #根据案例不同操作类型执行不同方法
    def test_Product_ImageTypeConfig(self):
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '新增':
            self.logstu.info(u"影像类型配置新增")
            self.add_Product_ImageTypeConfig()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '查询':
            self.logstu.info(u"影像类型配置查询")
            self.query_Product_ImageTypeConfig()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '删除':
            self.logstu.info(u"影像类型配置删除")
            self.del_Product_ImageTypeConfig()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '产品维护':
            self.logstu.info(u"商品影像文件配置：产品维护")
            self.Maintain_Product_ImageTypeConfig()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '影像维护':
            self.logstu.info(u"商品影像文件配置：影像维护")
            self.Maintain_Product_ImageTypeConfig()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '贷后资料维护':
            self.logstu.info(u"商品贷后影像文件配置：贷后资料维护")
            self.Maintain_Product_ImageTypeConfig()


    #影像文件配置新增
    def add_Product_ImageTypeConfig(self):
       #查询已有记录数，并在日志中打印出来
        self.pub.comeinifm('right','frameright','myiframe0')
        prerowcount = self.pub.table_getRowsCount()
        if prerowcount>=0:
            self.pub.table_RowClick(prerowcount)
            self.logstu.info(u"新增前记录总数为%s条" % prerowcount)
            pass
        else:
            self.logstu.info(u"新增前记录总数为%s条" % prerowcount)
        #进入新增按钮所在iframe，并点击新增按钮
        self.pub.comeinifm('right','frameright')
        self.pub.table_BtnClick_NoSetTimeOut(u'新增')
        ###进入到新增内容输入页面
        self.pub.comeinifm('right','frameright','myiframe0')
        #输入案例中要输入的字段值
        self.pub.setTableCellValueFast(self.dict_data,prerowcount+1,'right','frameright','myiframe0')
        #返回保存按钮所在iframe
        self.pub.comeinifm('right','frameright')
        # 点击保存按钮
        self.pub.table_BtnClick_NoSetTimeOut(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        #判断是否新增成功
        self.pub.comeinifm('right','frameright','myiframe0')
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
    def query_Product_ImageTypeConfig(self):
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[3] == '产品':
            self.pub.comeinifm('right','frameright','rightup')
            self.pub.selectAutoSets(self.dict_data)
            self.pub.comeinifm('right','frameright','rightup','myiframe0')
            rowcount = self.pub.table_getRowsCount()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[3] == '影像':
            self.pub.comeinifm('right','frameright','rightdown')
            self.pub.selectAutoSets(self.dict_data)
            self.pub.comeinifm('right','frameright','rightdown','myiframe0')
            rowcount = self.pub.table_getRowsCount()
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[3] == '1':
            #进入查询及其输入iframe  #输入查询参数，执行查询
            self.pub.comeinifm('right','frameright')
            self.pub.selectAutoSets(self.dict_data)
            #进入查询记录表单所在iframe
            self.pub.comeinifm('right','frameright','myiframe0')
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
        #返回主页面
        self.pub.comeinifm('right')

    ##影像类型配置删除方法
    def del_Product_ImageTypeConfig(self):
        #查询已有记录数，并在日志中打印出来
        self.pub.comeinifm('right','frameright')
        self.driver.implicitly_wait(6)
        #输入查询参数，执行查询
        self.pub.selectAutoSets(self.dict_data)
        #进入查询记录表单所在iframe
        self.pub.comeinifm('right','frameright','myiframe0')
        ##删除前记录数
        preTotalRows = self.pub.table_getRowsCount()
        self.logstu.info(u"表单删除前查询到%s记录数" % preTotalRows)
        #判断核列表中是否有记录
        if preTotalRows <=0:
            #列表无记录数执行该部分代码
            self.logstu.info(u"列表未查询到要删除的数据,无法执行删除记录操作")
            rowcount =''
            rul ='列表未查询到要删除的数据,无法执行删除记录操作'
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
            self.pub.comeinifm('right','frameright')
            self.pub.table_BtnClick_NoSetTimeOut(u'删除')
            self.logstu.info(u"表单中记录删除成功")
            rul ='表单中记录删除成功'
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.pub.comeinifm('right')
            pass

    #产品类型、影像文件维护
    def Maintain_Product_ImageTypeConfig(self):
        result = ''
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '产品维护':
            btnname = '产品维护'
            titlename = '选取产品类型'
            alerttext = '商品更新成功'
            result = self.pub.Maintain(self.dict_data,btnname,titlename,alerttext,'right','frameright','rightup')
            self.pub.comeinifm('right')
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '影像维护':
            btnname = '影像维护'
            titlename = '选取影像文件'
            alerttext = '影像文件操作成功'
            result = self.pub.Maintain(self.dict_data,btnname,titlename,alerttext,'right','frameright','rightdown')
            self.pub.comeinifm('right')
        if self.pub.all_type_to_encode(self.dict_data["操作类型"]).split('|')[2] == '贷后资料维护':
            btnname = '贷后资料维护'
            titlename = '选取影像文件'
            alerttext = '影像文件操作成功'
            result = self.pub.Maintain(self.dict_data,btnname,titlename,alerttext,'right','frameright','rightup')
            self.pub.comeinifm('right')

        self.logstu.info(u'运行结果%s'% (result))
        if result <>'':
            ruls = self.pub.all_type_to_encode(result).split('|')[0]
            left = self.pub.all_type_to_encode(result).split('|')[1]
            right = self.pub.all_type_to_encode(result).split('|')[2]
            if ruls==u'成功':
                self.logstu.info(u'%s运行结果:%s:,成功向左移动%s条数据，向右移动%s条数据'% (btnname,ruls,left,right))
                rul = u'%s运行结果:%s:,成功向左移动%s条数据，向右移动%s条数据'% (btnname,ruls,left,right)
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                pass
            else:
                self.logstu.info(u'%s运行结果:%s,未成功向右移动或向左移动任何一条记录'% (btnname,ruls))
                rul = u'%s运行结果:%s,未成功向右移动或向左移动任何一条记录'% (btnname,ruls)
                updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
                self.actdb.testCaseUpdate(updatestr)
                self.comeinifm('right')
                #引发断言错误
                self.assertEqual(1, 2)
        else:
            rul = u'未成功向右移动或向左移动任何一条记录，%s 失败'% (btnname)
            updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" % (self.actdb.casetitle_cn['执行结果'], rul, self.dict_data['test_id'])
            self.actdb.testCaseUpdate(updatestr)
            self.comeinifm('right')
            #引发断言错误
            self.assertEqual(1, 2)
