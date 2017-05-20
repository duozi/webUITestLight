#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest,xmlrunner,sys,time
sys.path.append(r'../..')
from Sys_Carloan.PageObj.PageLogin import PageLogin
from Sys_Carloan.PageObj.PageIndex import PageIndex
from selenium.common.exceptions import NoSuchElementException
from Utils.BaseTestClass import BaseTestClass
from Utils.UnitTestRultAct import UnitTestRultAct
from ddt import ddt,data,unpack
reload(sys)
sys.setdefaultencoding('utf8')

@ddt
class TestAdmin2(BaseTestClass):
    loginurl = 'http://10.18.12.61:8091/xncar/'
    captchaimage = 'http://10.18.12.61:8091/xncar/Login!captcha.action'
    captchavalue = 'http://10.18.12.61:8091/xncar/Login!getCaptcha.action'

    @classmethod
    def setUpClass(cls):
        '''
        测试类中所有测试方法执行前执行的方法
        '''
        super(TestAdmin2, cls).setUpClass() # 执行基类方法，初始化浏览器
        cls.pagelogin = PageLogin(cls.browserclass.get_driver()) # 实例化登录页面及操作类
        cls.pageindex = PageIndex(cls.browserclass.get_driver()) # 登录首页，提供左侧1、2级菜单操作



    def test_a_weblogin(self):
        """
        登录测试，并为后面的菜单页面check测试，提供登录后的系统操作
        :return:
        """
        self.log.info('--------- Start Login ---------')
        self.browserclass.get_driver().get(self.loginurl)

        captvalue = self.pagelogin.getcaptcha(self.loginurl, self.captchaimage,self.captchavalue)
        self.pagelogin.userlogin('admin','888888', captvalue)
        check = None
        try:
            check = self.browserclass.get_driver().find_element_by_link_text(u'密码修改')
        except NoSuchElementException as e:
            self.log.error(e)
            self.assertTrue(check!=None, u'NoSuchElementException: 登录失败，没有找到密码修改链接！')

    @data(('02业务管理', '01业务申请','', '第一步测算'),
          ('02业务管理', '02申请管理','', 'xxxxxx'),
          ('14参数配置', '任务分配管理', '组任务待办列表', ''))
    @unpack
    def test_b_pagecheck(self, menu1, menu2, menu3, check_a):
        """
        数据驱动，左侧菜单点击及页面显示check
        三个参数依次是 一级菜单 二级菜单 显示页面的a标签的文本
        :return:
        """
        self.log.info('--------- Start Page Check ---------')
        self.log.info('参数 [%s|%s|%s|%s]' % (menu1, menu2,menu3, check_a))
        self.pageindex.open_menu1(menu1)
        self.pageindex.open_menu2(menu2)
        tabname = ''
        if menu3 != "":
            tabname = menu3
            self.pageindex.open_menu3(menu3)
        else:
            tabname= menu2

        self.assertTrue(self.pageindex.tab_is_exist(tabname), '未找到 %s tab!' % tabname)
        #self.pageindex.tabs_act(tabname, 'Click')
        #self.pageindex.tabs_act(tabname, 'Refresh')
        if check_a != '':
            self.assertTrue(self.pageindex.tabcontentcheck(check_a), '未找到 %s 按钮!' % check_a)
        self.pageindex.tabs_act(tabname, 'Close')


if __name__ == '__main__':
    # 自定义 html 报告 txt 报告 xml报告
    suite = unittest.makeSuite(TestAdmin2)
    testRunner = xmlrunner.XMLTestRunner(output=sys.path[0] + '/output')
    testRunner.failfast = False
    testRunner.buffer = False
    testRunner.catchbreak = False
    var = testRunner.run(suite)
    caserult = UnitTestRultAct()
    caserult.CreateReport([caserult.get_TestCase(var)], strcode='gbk')
