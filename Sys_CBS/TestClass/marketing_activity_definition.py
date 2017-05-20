# -*- coding: utf-8 -*-

from Sys_CBS.PageObj.lyElementsOperation import PublicAct
import unittest, time


class marketing_activity_definition(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row =""          #接收main脚本传送的当前处理的行数

    def setUp(self):
        #self.driver = self.comm.get_browserdrvie('Chrome')
        self.driver = self.mainWebDr
        self.driver.implicitly_wait(30)
        self.accept_next_alert = True
        self.execldata = ""
        self.filepath = ""
        self.pub = PublicAct(self.driver)
        #进入具体菜单
        self.driver.implicitly_wait(6)
        self.pub.goto_menu(self.dict_data)
        print self.row

    def test_marketing_activity_definition(self):
        driver = self.driver
        if self.dict_data["操作类型"].encode('utf8') == '新建营销活动':
            self.logstu.info(u"新建营销活动")
            self.new_market_activity()
        if self.dict_data["操作类型"].encode('utf8') == '修改营销活动':
            self.logstu.info(u"修改营销活动")
            self.market_activity_modification()
        if self.dict_data["操作类型"].encode('utf8') == '停用营销活动':
            self.logstu.info(u"停用营销活动")
            self.change_activity_status("off")
        if self.dict_data["操作类型"].encode('utf8') == '启用营销活动':
            self.logstu.info(u"启用营销活动")
            self.change_activity_status("on")

    def new_market_activity(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'新增')
        ###进入到新增界面
        time.sleep(2)
        self.pub.input_values(self.dict_data,'strategy', 'right', 'myiframe0')
        # 点击保存按钮
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        if u"该营销活动已存在！" == text:
            #引发断言错误
            self.logstu.info(u"该营销活动已存在,新增失败")
            self.assertEqual(1, 2)
            pass
            # raise Exception(u'已经存在相同规则，请重新填写！')
        time.sleep(1)
        self.pub.timeoutBtnClick(u'返回')
        text = self.pub.is_alert_and_close_and_get_text()

    def market_activity_modification(self):
        driver = self.driver
        self.pub.comeinifm('right','myiframe0')
        self.pub.click_line_and_return_status(self.dict_data )
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u"详情")
        time.sleep(2)
        self.pub.input_values(self.dict_data,'strategy', 'right', 'myiframe0')
        # 点击保存按钮
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        if u"已经存在相同规则，请重新填写！" == text:
            self.logstu.info(u"该营销活动已存在,修改失败")
            #引发一个断言错误
            self.assertEqual(1, 2)
            pass
            # raise Exception(u'已经存在相同规则，请重新填写！')
        time.sleep(1)
        self.pub.timeoutBtnClick(u'返回')
        text1 = self.pub.is_alert_and_close_and_get_text()

    def change_activity_status(self,act):
        driver =self.driver
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.click_line_and_return_status(self.dict_data)
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u"停用/启用")
        text = self.pub.get_alert_text()
        self.logstu.info(u"alert text is %s" % text)
        if (act == "on" and u"启用" in text) or (act == "off" and u"停用" in text):
            self.pub.alert_accept_dismiss("accept")
            self.logstu.info(u"确定")
        else:
            self.pub.alert_accept_dismiss("dismiss")
            self.logstu.info(u"取消" )


