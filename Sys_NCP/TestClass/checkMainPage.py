#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest,xmlrunner,sys,time
sys.path.append(r'../..')
from Sys_NCP.PageObj.NCPLogin import NCPLogin
from Sys_NCP.PageObj.PageIndex import PageIndex
from selenium.common.exceptions import NoSuchElementException
from Utils.BaseTestClass import BaseTestClass
from Utils.UnitTestRultAct import UnitTestRultAct
from ddt import ddt,data,unpack
reload(sys)
sys.setdefaultencoding('utf8')

@ddt
class CheckMainPage(BaseTestClass):
    loginurl = 'http://10.18.12.15:8080/ncp-web'
    captchaimage = 'http://10.18.12.15:8080/ncp-web/pages/login.jsp'
    captchavalue = 'http://10.18.12.15:8080/ncp-web/pages/login.jsp'

    @classmethod
    def setUpClass(cls):
        '''
        测试类中所有测试方法执行前执行的方法
        '''
        super(CheckMainPage, cls).setUpClass() # 执行基类方法，初始化浏览器
        cls.pagelogin = NCPLogin(cls.browserclass.get_driver()) # 实例化登录页面及操作类
        cls.pageindex = PageIndex(cls.browserclass.get_driver()) # 登录首页，提供左侧1、2级菜单操作



    def test_a_weblogin(self):
        """
        登录测试，并为后面的菜单页面check测试，提供登录后的系统操作
        :return:
        """
        self.log.info('--------- Start Login ---------')
        self.browserclass.get_driver().get(self.loginurl)
        self.pagelogin.NCPuserlogin('admin', '88888888')

        check = None
        try:
            check = self.browserclass.get_driver().find_element_by_link_text(u'NEO Core Platform')
        except NoSuchElementException as e:
            self.log.error(e)
            self.assertTrue(check!=None, u'NoSuchElementException: 登录失败，没有找到NEO Core Platform链接！')
    @data(
        ('合同管理', '合同查询', '', '搜索'),
        ('合同管理', '商品贷-冻结合同', '', '合同详情'),
        ('合同管理', '商品贷-解冻合同', '', '合同详情'),
        ('合同管理', '现金贷-冻结合同', '', ''),
        ('合同管理', '现金贷-解冻合同', '', ''),
        ('合同管理', '合同撤销', '', '合同详情'),
        ('合同管理', '已撤销合同', '', '合同详情'),
        ('合同管理', '合同模板管理', '', '详情'),
        ('合同管理', '操作记录查询', '', ''),
        ('放款管理', '商品贷待发送付款合同', '', '搜索'),
        ('放款管理', '商品贷P2P已发送合同', '', '搜索'),
        ('放款管理', '商品贷信托已发送合同', '', '搜索'),
        ('放款管理', '现金贷已冻结合同', '', '搜索'),
        ('放款管理', '商品贷已冻结合同', '', '搜索'),
        ('放款管理', '商品贷付款失败合同', '', '搜索'),
        ('放款管理', '商品贷已付款合同', '', ''),
        ('放款管理', '现金贷待放款查询', '', '搜索'),
        ('放款管理', '现金贷P2P已发送合同', '', '搜索'),
        ('放款管理', '现金贷信托已发送合同', '', '搜索'),
        ('放款管理', '现金贷付款失败合同', '', '搜索'),
        ('放款管理', '现金贷已付款合同', '', '搜索'),
        ('放款管理', 'P2P商品贷回盘', '', ''),
        ('放款管理', '信托商品贷回盘', '', '搜索'),
        ('放款管理', 'P2P现金贷回盘', '', '搜索'),
        ('放款管理', '信托现金贷回盘', '', '搜索'),
        ('还款管理', '提前还款管理费登记', '', '搜索'),
        ('还款管理', '提前还款记录', '', '搜索'),
        ('还款管理', '强制还款', '', '搜索'),
        ('还款管理', '批量强制还款', '', '搜索'),
        ('还款管理', '已强制还款记录', '', '搜索'),
        ('还款管理', '手工入账', '', '搜索'),
        ('还款管理', '豁免审批', '', '搜索'),
        ('还款管理', '代扣记录查询', '', ''),
        ('还款管理', '借据查询', '', '搜索'),
        ('还款管理', '交易查询', '', '搜索'),
        ('退货退款退保管理', '退货审批', '', '搜索'),
        ('退货退款退保管理', '退货登记', '', '搜索'),
        ('退货退款退保管理', '退款登记', '', '搜索'),
        ('退货退款退保管理', '退保审批', '', '搜索'),
        ('退货退款退保管理', '提现审批', '', '搜索'),
        ('退货退款退保管理', '提现登记', '', '搜索'),
        ('客户管理', '修改姓名审批', '', ''),
        ('客户管理', '代扣账号变更审批', '', ''),
        ('账户管理', '账户综合信息查询', '', '搜索'),
        ('账户管理', '现金账户信息管理', '', '搜索'),
        ('账户管理', '贷款账户信息管理', '', '搜索'),
        ('账户管理', '现金账户流水查询', '', '搜索'),
        ('账户管理', '贷款账户流水查询', '', '搜索'),
        ('系统管理', '角色管理', '', '搜索'),
        ('系统管理', '组织架构管理', '', '检索'),
        ('系统管理', '菜单管理', '', '搜索'),
        ('系统管理', '用户转移', '', '搜索'),
        ('系统管理', '参数管理', '', '搜索'),
        ('系统管理', '快付通白名单管理', '', '搜索'),
        ('系统管理', '日志管理', '', '搜索'),
        )
    @unpack
    def test_b_pagecheck(self, menu1, menu2, menu3, check_a):
        """
        数据驱动，左侧菜单点击及页面显示check
        三个参数依次是 一级菜单 二级菜单 显示页面的a标签的文本
        :return:
        """
        self.log.info('--------- Start Page Check ---------')
        self.log.info('参数 [%s|%s|%s|%s]' % (menu1, menu2,menu3, check_a))
        self.pagelogin.get_loginStatus('admin', '88888888')
        self.pageindex.open_menu1(menu1)
        self.pageindex.open_menu2(menu1,menu2)
        tabname = ''
        if menu3 != "":
            tabname = menu3
            self.pageindex.open_menu3(menu3)
        else:
            tabname= menu2

        self.assertTrue(self.pageindex.tab_is_exist(tabname), '未找到 %s tab!' % tabname)
        if check_a != '':
            self.assertTrue(self.pageindex.tabcontentcheck(check_a), '未找到 %s 按钮!' % check_a)
        self.pageindex.tabs_act(tabname, 'Close')


if __name__ == '__main__':
    # 自定义 html 报告 txt 报告 xml报告
    suite = unittest.makeSuite(CheckMainPage)
    testRunner = xmlrunner.XMLTestRunner(output=sys.path[0] + '/output')
    testRunner.failfast = False
    testRunner.buffer = False
    testRunner.catchbreak = False
    var = testRunner.run(suite)
    caserult = UnitTestRultAct()
    caserult.CreateReport([caserult.get_TestCase(var)], strcode='gbk')
