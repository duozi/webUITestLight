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
class TestAdmin(BaseTestClass):
    loginurl = 'http://10.18.12.61:8091/xncar/'
    captchaimage = 'http://10.18.12.61:8091/xncar/Login!captcha.action'
    captchavalue = 'http://10.18.12.61:8091/xncar/Login!getCaptcha.action'

    @classmethod
    def setUpClass(cls):
        '''
        测试类中所有测试方法执行前执行的方法
        '''
        super(TestAdmin, cls).setUpClass() # 执行基类方法，初始化浏览器
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

    @data(('01我的任务', '待办任务','', '历史1'),
          ('02业务管理', '01业务申请','', '第一步测算'),
          ('02业务管理', '02申请管理','', '查询'),
          ('02业务管理', '03家访台账','', '查询'),
          ('02业务管理', '04合同签订','', '搜 索'),
          ('02业务管理', '05合同信息','', '查询'),
          ('02业务管理', '06放款申请','', '查询'),
          ('02业务管理', '07撤销管理','', '查询'),
          ('02业务管理', '08征信报告','', '查   询  '),
          ('02业务管理', 'GPS管理','', '查询'),
          ('02业务管理', '流程监管','', '查询'),
          ('03放款管理', '待放款','', '查询'),
          ('03放款管理', '放款回执上传','', '查询'),
          ('03放款管理', '已发送','', '查询'),
          ('03放款管理', '放款导入','', '查询'),
          ('03放款管理', '放款后督','', '查询'),
          ('03放款管理', '已放款','', '查询'),
          ('03放款管理', '放款日志','', '查   询   '),
          ('04贷后管理', '01贷后客户管理','', '查询'),
          ('04贷后管理', '02客户对账管理','', '查询'),
          ('04贷后管理', '03还款计划表','', '查   询   '),
          ('05档案管理', '档案归档','', '查询'),
          ('05档案管理', '档案柜编码','', '查询'),
          ('05档案管理', '借阅管理','', '清空'),
          ('05档案管理', '档案移交','', '查询'),
          ('06保险管理', '保险管理','', '查 询'),
          ('06保险管理', '理赔管理','', '保存'),
          ('06保险管理', '续保管理','', '查 询'),
          ('06保险管理', '险种配置','', '查询'),
          ('07资金管理', '租金管理', '还款核销', '查询'),
          ('07资金管理', '租金管理', '还款录入', '查询'),
          ('07资金管理', '租金管理', '还款提醒', '查询'),
          ('07资金管理', '租金管理', '首期款核销', '查询'),
          ('07资金管理', '租金管理', '租金代扣导出', '查询'),
          ('07资金管理', '租金管理', '租金代扣回执', '查询回执结果'),
          ('07资金管理', '租金管理', '租金代扣回执结果', '查询'),
          ('07资金管理', '租金管理', '应扣未扣查询', '查询'),
          ('07资金管理', '租金管理', '代扣记录查询', '查询'),
          ('07资金管理', '租金管理', '实时代扣', '查   询   '),
          ('07资金管理', '还款记录', '租金-核销单查询', '查询'),
          ('07资金管理', '还款记录', '租金-核销明细', '查询'),
          ('07资金管理', '罚息管理', '减免查询', '查询'),
          ('07资金管理', '罚息管理', '减免罚息', '搜 索'),
          ('08催收管理', '催收管理', '', '催收信息'),
          ('08催收管理', '电话催收', '', '查询'),
          ('08催收管理', '现场催收', '', '查询'),
          ('09报表管理', '放款报表', '', '查询'),
          ('09报表管理', '项目统计', '业务统计报表', '查询'),
          ('09报表管理', '超级表统计', '', '查询'),
          ('09报表管理', '风险成因', '', '查询'),
          ('09报表管理', '流程统计', '正常流程统计', '查询'),
          ('09报表管理', '流程统计', '异常流程统计', '查询'),
          ('09报表管理', '逾期报表', '逾期率报表', '查询'),
          ('09报表管理', '逾期报表', '逾期金额报表', '查询'),
          ('09报表管理', '逾期报表', '逾期期次报表', '查询'),
          ('09报表管理', '逾期报表', '项目逾期率', '查询'),
          ('10业务结束', '01提前结清处理', '', '查 询'),
          ('10业务结束', '02提前结清查询', '', '查 询'),
          ('10业务结束', '03项目回购处理', '', '查 询'),
          ('10业务结束', '04项目回购查询', '', '查 询'),
          ('11接口管理', '公安', '认证', '认 证'),
          ('11接口管理', '公安', '认证日志', '查 询'),
          ('11接口管理', '公安', '认证通过查询', '查 询'),
          ('11接口管理', '公安', '调用认证接口查询', '查 询'),
          ('11接口管理', '短信', '短信接口配置', ''),
          ('11接口管理', '短信', '发送短信', '发 送'),
          ('12合作机构', 'SP管理', '', '查询'),
          ('12合作机构', '保险公司', '', '查询'),
          ('12合作机构', '经销商管理', '', '查询'),
          ('13权限管理', '任务分配', '', '查询'),
          ('13权限管理', '组织架构', '', '刷新'),
          ('13权限管理', '系统授权', '', '查询'),
          ('13权限管理', '菜单配置', '', ' 上传菜单图标 '),
          ('13权限管理', '系统信息', '', '清理文件缓存'),
          ('13权限管理', '人员管理', '', '查询'),
          ('13权限管理', '计划任务', '', '启动所有任务'),
          ('13权限管理', '操作日志', '', '查询'),
          ('13权限管理', '业务模块维护', '', '查询'),
          ('13权限管理', '跟踪配置', '', '清空添加新配置'),
          ('13权限管理', '行业管理', '', '查询'),
          ('13权限管理', '流程定义', '', '查询'),
          ('13权限管理', '流程任务人管理', '', '查询'),
          ('14参数配置', '01公司信息维护', '', ''),
          ('14参数配置', '调息管理', '', ''),
          ('14参数配置', '资金额度配置', '', ''),
          ('14参数配置', '资金匹配', '', ''),
          ('14参数配置', '02销售区域维护', '', ''),
          ('14参数配置', '03金融产品维护', '', ''),
          ('14参数配置', '关键日期配置', '', ''),
          ('14参数配置', '基础利率', '', ''),
          ('14参数配置', '模板关联', '', ''),
          ('14参数配置', '模板管理', '', ''),
          ('14参数配置', '模板组管理', '', ''),
          ('14参数配置', '行政区域划分', '', ''),
          ('14参数配置', '账号维护', '', ''),
          ('14参数配置', '厂商管理', '', ''),
          ('14参数配置', '车型数据', '', ''),
          ('14参数配置', '数据字典', '', ''),
          ('14参数配置', 'SQL设置', '', ''),
          ('14参数配置', '编码设置', '', ''),
          ('14参数配置', 'APP版本维护', '', ''),
          ('14参数配置', '公告管理', '', ''),
          ('14参数配置', '推送模版设置', '', ''),
          ('14参数配置', '系统设置', '', ''),
          ('14参数配置', '政策发布', '', ''),
          ('14参数配置', '资料管理', '', ''),
          ('14参数配置', '设定起租日', '', ''),
          ('14参数配置', '任务分配管理', '任务分配规则管理', ''),
          ('14参数配置', '任务分配管理', '任务组管理', ''),
          ('14参数配置', '任务分配管理', '任务组规则', ''),
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
    suite = unittest.makeSuite(TestAdmin)
    testRunner = xmlrunner.XMLTestRunner(output=sys.path[0] + '/output')
    testRunner.failfast = False
    testRunner.buffer = False
    testRunner.catchbreak = False
    var = testRunner.run(suite)
    caserult = UnitTestRultAct()
    caserult.CreateReport([caserult.get_TestCase(var)], strcode='gbk')
