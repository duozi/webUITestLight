# -*- coding: utf-8 -*-
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from Sys_CBS.PageObj.salesmanFunction import SalesmanFunction
import unittest, time

#create by limeng
class SalesmanChangeApply(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    row =""          #接收main脚本传送的当前处理的行数


    def setUp(self):
        #self.driver = self.comm.get_browserdrvie('Chrome')
        self.driver = self.mainWebDr
        self.driver.implicitly_wait(30)
        self.pub = PublicAct(self.driver)
        self.salesman = SalesmanFunction(self.driver)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.execldata = ""
        self.filepath = ""
        #进入具体菜单
        #self.comm.goto_menu(self.driver,self.row)
        self.pub.goto_menu(self.dict_data)

    def test_SalesmanChangeApply(self):
        driver = self.driver
        if self.dict_data["操作类型"].encode('utf8') == '新增申请':
            self.new_application()
            time.sleep(5)


    def new_application(self):
        self.logstu.info(u"新增申请")
        driver = self.driver
        #读取编号
        #sale_no = self.dict_data['查询条件1'].split('|')[1]
        #sale_no = '2016030900000191'
        #销售人员变更数据
        key1 = self.pub.all_type_to_unicode(self.dict_data['输入值1'].split('|')[0])
        key2 = self.pub.all_type_to_unicode(self.dict_data['输入值2'].split('|')[0])
        date1 = self.dict_data['输入值1'].split('|')[1]
        date2 = self.dict_data['输入值2'].split('|')[1]
        date_dict = { key1: date1 ,key2: date2 }
        # 点击新增申请
        self.pub.comeinifm('right')
        self.pub.thread_btn('新增申请')
        # 点击选择按钮"。。。"
        time.sleep(3)
        self.pub.comeinifm('ObjectList', 'myiframe0')
        self.pub.thread_btn2(driver.find_element_by_class_name('inputdate'))
        # #
        # self.pub.comeinifm('ObjectList')
        # self.pub.click_btn(driver.find_element_by_id('FilterIconPlus'))点击查询条件
        # # 查询条件填入内容
        # self.pub.input_text(driver.find_element_by_name('DOFILTER_DF0_1_VALUE'), sale_no)
        # self.pub.select_btn(u'查询')
        # time.sleep(5)
        self.pub.comeinifm('ObjectList', 'myiframe0')
        # self.pub.click_btn(driver.find_element_by_css_selector("input[value='%s']" % sale_no))
        #选择第一条数据
        self.pub.click_btn(driver.find_element_by_css_selector("input[name='R0F0']"  ))
        #得到省份证号码
        cert_id = driver.find_element_by_css_selector("input[name='R0F2']").get_attribute('value')
        driver.switch_to_default_content()
        time.sleep(3)
        # 点击确认，退出选择界面
        self.pub.thread_btn2(driver.find_element_by_css_selector('input[value="确认"]'))
        # 选择变更类型
        time.sleep(2)
        self.pub.comeinifm('ObjectList', 'myiframe0')
        s = driver.find_element_by_name("R0F3")
        time.sleep(2)
        s.find_element_by_xpath("//option[@value='10']").click()
        # 点击确认，退出新增窗口
        self.pub.comeinifm('ObjectList')
        self.pub.thread_btn('确认')
        #返回主业务系统，选择销售人员，填写变更信息
        time.sleep(2)
        #cert_id = '44010019850602088X'
        self.pub.comeinifm('right')
        self.pub.selectAutoSet(u'身份证号', u'等于', cert_id)
        self.pub.select_btn(u'查询')
        self.pub.comeinifm('right', 'myiframe0')
        time.sleep(1)
        self.pub.click_btn(driver.find_element_by_css_selector("input[value='%s']" % cert_id))
        self.pub.comeinifm('right')
        self.pub.thread_btn('申请详情')
        self.pub.comeinifm('ObjectList', 'myiframe0')
        self.pub.input_text(driver.find_element_by_id('R0F14'), date_dict[u'电子邮箱'])
        #js = "document.getElementByName('R0F14').value='%s'" %date_dict[key1]
        #driver.execute_script(js)
        self.logstu.info(u"电子邮箱填写为%s" %date_dict[u'电子邮箱'])
        time.sleep(2)
        self.pub.input_text(driver.find_element_by_id('R0F16'), date_dict[u'移动电话'])
        self.logstu.info(u"移动电话填写为%s" % date_dict[u'移动电话'])
        time.sleep(2)
        self.logstu.info(u"选择上级")
        self.pub.thread_btn2(driver.find_element_by_css_selector("input[value='选择上级']"))
        self.pub.comeinifm('ObjectList', 'myiframe0')
        self.pub.click_btn(driver.find_element_by_css_selector("input[name='R0F0']"))
        driver.switch_to_default_content()
        time.sleep(2)
        self.pub.thread_btn2(driver.find_element_by_css_selector('input[value="确认"]'))
        self.logstu.info(u"修改完毕，点击保存")
        self.pub.comeinifm('ObjectList')
        self.pub.table_BtnClick_NoSetTimeOut('保存')
        driver.switch_to_default_content()
        #关闭当前窗口
        self.pub.winClose()
        # 点击提交,申请结束
        time.sleep(2)
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.click_btn(driver.find_element_by_css_selector("input[value='%s']" % cert_id))
        self.pub.comeinifm('right')
        self.pub.thread_btn('提交')
        #关闭alert窗口
        self.pub.close_alert_and_get_its_text()
        #提取出身份证号码，写到excel中
        value = cert_id
        #self.comm.write_file(value, self.row, self.comm.get_key_cell_col("执行结果"))
        updatesql = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], value, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatesql)




