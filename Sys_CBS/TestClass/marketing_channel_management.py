# -*- coding: utf-8 -*-

from Sys_CBS.PageObj.lyElementsOperation import PublicAct
import unittest, time

class marketing_channel_management(unittest.TestCase):
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数


    def setUp(self):
        # self.driver = self.comm.get_browserdrvie('Chrome')
        self.driver = self.mainWebDr
        self.driver.implicitly_wait(30)
        self.accept_next_alert = True
        self.execldata = ""
        self.filepath = ""
        self.pub = PublicAct(self.driver)
        # 进入具体菜单
        self.driver.implicitly_wait(6)
        self.pub.goto_menu(self.dict_data)
        print self.row

    def test_marketing_channel_management(self):
        driver = self.driver
        if self.dict_data["操作类型"].encode('utf8') == '新增渠道':
            self.logstu.info(u"新增渠道")
            self.new_channel()
        if self.dict_data["操作类型"].encode('utf8') == '修改渠道':
            self.logstu.info(u"修改渠道")
            self.modify_channel()

    def new_channel(self):
        #渠道中暂时无法新增
        pass
        # driver = self.driver
        # self.pub.comeinifm('right')
        # self.pub.timeoutBtnClick(u'新增')
        # ###进入到新增界面
        # time.sleep(2)
        # self.pub.input_values(self.dict_data,'channel', 'right', 'myiframe0')
        # # 点击保存按钮
        # self.pub.comeinifm('right')
        # self.pub.timeoutBtnClick(u'保存')
        # text = self.pub.is_alert_and_close_and_get_text()
        # self.logstu.info(u"alert text is %s" % text)
        # if u"该营销活动已存在！" == text:
        #     pass
        #     # raise Exception(u'已经存在相同规则，请重新填写！')
        # time.sleep(1)
        # self.pub.timeoutBtnClick(u'返回')

    def modify_channel(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.selectAutoSets(self.dict_data)
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        # 查看有多少条数据
        rnum = self.pub.table_getRowsCount()
        cnum = self.pub.table_getColumnsCount()
        self.pub.logstu.debug(u'行数：%s.列数：%s' % (rnum, cnum))
        if rnum == 0:
            self.pub.logstu.info(u"没有查询出来数据，结束")
            return
        self.table_RowClick(0)
        time.sleep(1)
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'详情')
        time.sleep(1)
        self.pub.comeinifm('right')
        btns = driver.find_elements_by_css_selector("div.btn_text")
        for i in range(len(btns)):
            if btns[i].text == u"保存":
                break
            elif i == len(btns) - 1:
                self.logstu.info(u"页面没有保存按钮，页面默认不可以修改，结束")
                return
        # 修改内容
        self.pub.input_values(self.dict_data,'channel', 'right', 'myiframe0')
        # 保存按钮
        self.pub.comeinifm('right')
        self.pub.timeoutBtnClick(u'保存')
        text = self.pub.is_alert_and_close_and_get_text()
        self.logstu.info(u"alert text is %s" % text)
        time.sleep(1)
        self.pub.timeoutBtnClick(u'返回')
        if u"已经存在相同规则，请重新填写！" == text:
            #引发断言错误
            self.assertEqual(1, 2)
            pass
            # raise Exception(u'已经存在相同规则，请重新填写！')

    def table_RowClick(self, rownum):
        driver = self.driver
        try:
            driver.find_elements(*self.pub.table_tr)[rownum + 2].find_elements_by_tag_name('td')[1].click()
        except Exception as e:
            self.logstu.error(e)




