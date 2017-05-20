#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest,xmlrunner,sys,time
sys.path.append(r'../..')
from Sys_CBS.PageObj.CBSLogin import CBSLogin
from selenium import webdriver
from Sys_CBS.PageObj.PageIndex import PageIndex
from selenium.common.exceptions import NoSuchElementException
from Utils.BaseTestClass import BaseTestClass
from Utils.UnitTestRultAct import UnitTestRultAct
from ddt import ddt,data,unpack
reload(sys)
sys.setdefaultencoding('utf8')

@ddt
class CheckMainPage(BaseTestClass):
    loginurl = 'http://10.18.12.11:7001/XiaoNiu/'
    captchaimage = 'http://10.18.12.11:7001/XiaoNiu/logon.html'
    captchavalue = 'http://10.18.12.11:7001/XiaoNiu/logon.html'
    driver = 'Chrome'

    @classmethod
    def setUpClass(cls):
        '''
        测试类中所有测试方法执行前执行的方法
        '''
        super(CheckMainPage, cls).setUpClass() # 执行基类方法，初始化浏览器
        # cls.driver = webdriver.Chrome()
        # driver = 'Chrome'
        cls.pagelogin = CBSLogin(cls.browserclass.get_driver()) # 实例化登录页面及操作类
        # cls.pagelogin = CBSLogin(webdriver.Chrome())  # 实例化登录页面及操作类
        cls.pageindex = PageIndex(cls.browserclass.get_driver()) # 登录首页，提供左侧1、2级菜单操作



    def test_a_weblogin(self):
        """
        登录测试，并为后面的菜单页面check测试，提供登录后的系统操作
        :return:
        """
        self.log.info('--------- Start Login ---------')
        self.browserclass.get_driver().get(self.loginurl)
        self.pagelogin.userlogin('admin', '!000000als')

        check = None
        try:
            check = self.browserclass.get_driver().find_element_by_link_text(u'日常工作提示')
        except NoSuchElementException as e:
            self.log.error(e)
            self.assertTrue(check!=None, u'NoSuchElementException: 登录失败，没有找到\'日常工作提示\'链接！')
    @data(
        ('产品管理', '产品系列', '商品贷产品系列', '查询条件'),
        ('产品管理', '产品系列', '现金贷产品系列', '查询条件'),
        ('产品管理', '产品配置', '商品贷产品配置', '查询条件'),
        ('产品管理', '产品配置', '现金贷产品配置', '查询条件'),
        ('产品管理', '费用维护', '', '查询条件'),
        ('产品管理', '商品类型', '', '查询条件'),
        ('产品管理', '核算参数定义', '核算交易定义', '分录模板'),
        ('产品管理', '核算参数定义', '账务代码定义', '客户余额分类'),
        ('产品管理', '核算参数定义', '业务组件管理', '查询条件'),
        ('产品管理', '影像类型配置', '', '查询条件'),
        ('营销策略管理', '营销活动定义', '', '新增'),
        ('营销策略管理', '电销规则策略', '', '查询条件'),
        ('营销策略管理', '短信推广策略', '', '查询条件'),
        ('营销策略管理', '微信推广策略', '', '查询条件'),
        ('营销策略管理', '渠道管理', '', '查询条件'),
        ('渠道管理', '区域管理', '', '新增'),
        ('渠道管理', '商户门店管理', '商户门店准入申请', '查询条件'),
        ('渠道管理', '商户门店管理', '商户门店准入审批', '查询条件'),
        ('渠道管理', '商户门店管理', '门店准入申请', '查询条件'),
        ('渠道管理', '商户门店管理', '门店准入审批', '查询条件'),
        ('渠道管理', '商户门店管理', '商户信息变更申请', '查询条件'),
        ('渠道管理', '商户门店管理', '商户信息变更审核', '查询条件'),
        ('渠道管理', '商户门店管理', '门店信息变更申请', '查询条件'),
        ('渠道管理', '商户门店管理', '门店信息变更审核', '查询条件'),
        ('渠道管理', '商户门店管理', '商户管理', '查询条件'),
        ('渠道管理', '商户门店管理', '门店管理', '查询条件'),
        ('渠道管理', '商户门店管理', '门店设备申请', '查询条件'),
        ('渠道管理', '商户门店管理', '门店设备申请审核', '查询条件'),
        ('渠道管理', '银行账号信息管理', '银行账号申请', '查询条件'),
        ('渠道管理', '银行账号信息管理', '银行账号审批', '查询条件'),
        ('渠道管理', '银行代码管理', '', '查询条件'),
        ('渠道管理', '代扣渠道维护', '', '新增'),
        ('渠道管理', '保险供应商管理', '', '查询条件'),
        ('销售人员入职管理', '销售人员入职申请', '', '查询条件'),
        ('销售人员入职管理', '销售人员信息变更申请', '', '查询条件'),
        ('销售人员入职管理', '销售人员入职审核', '', '待处理申请'),
        ('销售人员入职管理', '销售人员变更审核', '', '待处理申请'),
        ('销售人员入职管理', '培训结果登记', '', '查询条件'),
        ('销售人员入职管理', '销售人员状态变更处理', '', '查询条件'),
        ('贷款审查', '贷款审批', '', '查询条件'), #当前工作
        ('贷款审查', '流程监控', '', '流程工作监控'),
        ('贷款审查', '合同管理', '合同撤销', '查询条件'),
        ('财务管理', '批量付款管理', '商品贷', '查询条件'), #待发送付款合同
        ('财务管理', '批量付款管理', '现金贷', '查询条件'),
        ('财务管理', '合同冻结付款管理', '商品贷', '查询条件'),
        ('财务管理', '合同冻结付款管理', '现金贷', '查询条件'),
        ('财务管理', '退款登记', '', '查询条件'),
        ('财务管理', '退款复核', '', '查询条件'),
        ('财务管理', '退货登记', '', '查询条件'),
        ('财务管理', '小牛在线每日放款检查', '商品贷', '查询条件'),
        ('财务管理', '小牛在线每日放款检查', '现金贷', '查询条件'),
        ('财务管理', '商户奖励金管理', '', '查询条件'),
        ('财务管理', '商户贴息管理', '', '查询条件'),
        ('贷后管理', '退款审批', '', '查询条件'),
        ('贷后管理', '退货审批', '', '查询条件'),
        ('贷后管理', '退保审批', '', '查询条件'),
        ('贷后管理', '代扣账号变更审批', '', '查询条件'),
        ('贷后管理', '期款豁免复核', '', '查询条件'),
        ('贷后管理', '强制还款', '', '查询条件'),
        ('贷后管理', '更改客户姓名审批', '', '查询条件'),
        ('贷后管理', '手工入账', '', '查询条件'),
        ('贷后管理', '手工入账复核', '', '查询条件'),
        ('贷后管理', '服务贷退款', '', '提交'),
        ('贷后管理', '实时代扣', '', '确定'),
        ('统计查询', '商户查询', '', '查询条件'),
        ('统计查询', '门店查询', '', '查询条件'),
        ('统计查询', '合同查询', '', '查询条件'),
        ('统计查询', '销售合同查询', '', '查询条件'),
        ('统计查询', '还款文件查询', '', '查询条件'),
        ('统计查询', '代扣记录查询', '', '查询条件'),
        ('统计查询', '销售信息查询', '', '查询条件'),
        ('统计查询', '交叉查询', '', '查询条件'),
        ('系统管理', '部门管理', '', '查询条件'),
        ('系统管理', '用户管理', '', '查询条件'),
        ('系统管理', '角色管理', '', '查询条件'),
        ('系统管理', '热部署管理', '', '离线'),
        ('系统管理', '综合信息', '', '通知管理'),
        ('参数管理', '自动豁免参数维护', '', '保存'),
        ('参数管理', '代码管理', '', '0.系统参数管理'),
        ('参数管理', '审批配置', '', '查询条件'),
        ('参数管理', '方法配置', '', '查询条件'),
        ('参数管理', '取消合同参数', '', '保存'),
        ('参数管理', '错误类型参数', '', '查询条件'),
        ('参数管理', '消费贷参数', 'app秒拒延时参数配置', '保存'),
        ('参数管理', '消费贷参数', '黑名单管理', '查询条件'),
        ('参数管理', '消费贷参数', '优质雇主名单管理', '查询条件'),
        ('参数管理', '消费贷参数', '社保信息查询维护', '查询条件'),
        ('参数管理', '消费贷参数', '临近城市维护', '查询条件'),
        ('参数管理', '消费贷参数', '门店分组代码维护', '查询条件'),
        ('参数管理', '消费贷参数', '超期未注册期限配置', '保存'),
        ('参数管理', '消费贷参数', '提前还款申请提前天数配置', '保存'),
        ('参数管理', '消费贷参数', 'GSPN维护', '查询条件'),
        ('参数管理', '消费贷参数', 'IMEI/VIN码验证配置', '保存'),
        ('参数管理', '审核要点管理', '流程阶段审核要点', '查询条件'),
        ('参数管理', '自动取消合同天数维护', '', '保存'),
        ('参数管理', '短信模板配置', '', '详情'),
        ('参数管理', 'Pad参数配置', '', '查询条件'),
        ('参数管理', '第三方接口参数配置', '', '鹏元人脸识别'),
        ('参数管理', '规则引擎配置', '', '新增'),
        ('参数管理', '贷后参数配置', '', '查询条件'),
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
        self.pagelogin.get_loginStatus('admin', '!000000als')
        self.pageindex.goto_menu(menu1, menu2, menu3)
        if menu3 == '':
            checkmenu = menu2
        else:
            checkmenu = menu3
        if check_a != '':
            self.assertTrue(self.pageindex.tabcontentcheck(checkmenu,check_a), '未找到 %s 按钮!' % check_a)
        # self.pageindex.tabs_act(tabname, 'Close')


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
