# -*- coding: utf-8 -*-
import unittest,time
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
from selenium.common.exceptions import NoAlertPresentException,UnexpectedAlertPresentException,NoSuchElementException
from selenium.webdriver.common.by import By

class LoanApprove(unittest.TestCase):
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象
    ##当前待办任务 - > '当前流程'字段
    current_process = (By.CSS_SELECTOR, "input[name=\"R0F17\"]")
    #####当前待办任务 - > '进件申请编号'字段
    Contract_Num = (By.CSS_SELECTOR, "input[name=\"R0F1\"]")
    #####CE专家审核的拒绝原因弹窗的 '确认' 按钮
    Confirm = (By.CSS_SELECTOR, "input[type=\"button\"][name=\"ok\"]")
    ##########已完成的任务 - > '当前阶段流程' 字段
    current_stage = (By.CSS_SELECTOR,"input[name=\"R0F19\"]")

    def setUp(self):
        # self.driver = self.comm.get_browserdrvie('Chrome')
        self.driver = self.mainWebDr
        self.driver.implicitly_wait(6)
        self.verificationErrors = []
        self.acccept_next_alert = True
        self.execldata = ""
        self.filepath = ""
        self.pub = PublicAct(self.driver)
        # self.Fun = Function()


        # 进入具体菜单
        # self.comm.goto_menu(self.driver,self.row)
        self.pub.goto_menu(self.dict_data)

    def test_LoanApprove(self):
        driver = self.driver
        if self.dict_data["操作类型"].split('|')[1] == u'贷款审批流程':
            self.logstu.info(u'贷款审批流程')
            self.loan_approve_process()
        if self.dict_data["操作类型"].split('|')[1] == u'CE专家审核通过':
            self.logstu.info(u'CE专家审核通过流程')
            self.CE_approve_pass()
        if self.dict_data["操作类型"].split('|')[1] == u'CE专家审核拒绝':
            self.logstu.info(u'CE专家审核拒绝流程')
            self.CE_approve_pass()


    def CE_approve_pass(self):
        driver = self.driver

        self.pub.leftMenuVagueClick(u'当前工作>当前待办任务', 'left')
        self.pub.comeinifm('right', 'myiframe0')
        cont = driver.find_element(*self.Contract_Num).get_attribute('value')
        self.pub.logstu.debug('进件申请编号:'+cont)
        # 选中列表第一行记录
        self.pub.table_RowClick(-2)
        driver.switch_to_default_content()
        self.pub.comeinifm('right')
        self.pub.table_BtnClick(u'签署意见')
        driver.switch_to_default_content()

        ######### 开始执行百度办公室电话核查
        text = self.get_Text1()
        for i in range(1,4):
            self.logstu.debug(u'CE审核流程 --- >'+self.get_Text1())
            str_in = '输入值' + str(i)
            opinion = self.dict_data[str_in].split('|')[2]
            remark = self.dict_data[str_in].split('|')[4]
            stagename = self.get_Text1()
            if stagename == self.dict_data[str_in].split('|')[0]:
                self.choose_opinions_Set_remarks(opinion,remark)
                self.Next_CheckBtnClick()

        ########## CE专家审核---通过
        result = self.dict_data['输入值4'].split('|')[2]
        rownum = self.dict_data['输入值4'].split('|')[4]
        remarks = self.dict_data['输入值4'].split('|')[6]
        self.CE_Approver(result, rownum, remarks)

        #######完成CE审核后，检查数据状态
        driver.switch_to_default_content()

        self.pub.leftMenuVagueClick(u'已完成工作>已完成的任务', 'left')
        self.pub.comeinifm('right')
        cont = 'FP09582016072000000058'
        self.pub.selectAutoSet(u'进件申请编号',u'等于',cont)
        self.logstu.debug('进件申请编号:'+cont)
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()
        self.pub.comeinifm('right','myiframe0')
        trs = driver.find_elements_by_tag_name('tr')
        self.logstu.debug("长度:")
        self.logstu.debug(len(trs))
        if len(trs) == 3:
            stagename = driver.find_element(*self.current_stage).get_attribute('value')
            self.logstu.debug(u'当前流程阶段：'+stagename)
            driver.switch_to_default_content()
            self.assertEqual(stagename,self.dict_data['预期结果'].split('|')[1])
        else:
            raise Exception('在已完成的任务中未查询到数据')



    def CE_approve_reject(self):
        driver = self.driver
        ######### 开始执行百度办公室电话核查
        for i in range(1, 4):
            str_in = '输入值' + str(i)
            opinion = self.dict_data[str_in].split('|')[2]
            remark = self.dict_data[str_in].split('|')[4]
            self.choose_opinions_Set_remarks(opinion, remark)
            self.Next_CheckBtnClick()
        ########## CE专家审核---拒绝
        result = self.dict_data['输入值4'].split('|')[2]
        rownum = self.dict_data['输入值4'].split('|')[4]
        remarks = self.dict_data['输入值4'].split('|')[6]
        self.CE_Approver(result, rownum, remarks)

###1、进入待办任务后，先做查询，判断当前行数是否大于3 ，
### a、行数小于 3，说明无任务，直接走新数据审批流程，点击获取任务按钮获取任务，先点击左侧的待办任务，获取进件编号和当前流程，用于后续的判断
### b、行数大于3，说明当前存在数据，判断是否存在在途数据，如有，先执行在途数据审批，再重新获取新数据，执行新数据审批
    def loan_approve_process(self):
        driver = self.driver
        self.pub.leftMenuVagueClick(u'当前工作>当前待办任务', 'left')
        self.pub.comeinifm('right')
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()
        self.get_task()  ###获取新任务
        Value1 = self.get_Value()
        time.sleep(1)
        ################ 完成 在途数据 的审批
        text = self.get_Text1()
        if (Value1 <> u'bib流程' and text != u'NCIIC手动身份核查' and text != u'文件检查') or\
            (Value1 == u'bib流程' and text != u'NCIIC手动身份核查'):
            self.get_flow1()
            self.get_task()
            Value2 = self.get_Value()
            self.get_flow2(Value2)            #########开始审批 新任务 ，按各流程执行不同的节点
        else:
            self.logstu.debug(u'无在途数据')
            self.get_flow2(Value1)#########开始审批 新任务 ，按各流程执行不同的节点
        driver.implicitly_wait(10)
        for i in range(0,5):
            time.sleep(1)
            self.logstu.debug(u'重复第'+ str(i) +u'次')
            try:
                if driver.switch_to_alert():
                    alert_text = driver.switch_to_alert().text
                    driver.switch_to_alert().accept()
                    break
            except NoAlertPresentException as e:
                self.logstu.error(e)
        self.logstu.debug(alert_text)
        self.logstu.debug(alert_text.strip(u'！'))
        self.logstu.debug(self.dict_data['预期结果'].split('|')[0])
        self.assertEqual(alert_text.strip(u'！'), self.dict_data['预期结果'].split('|')[0])

    #获取任务，当列表中有一条记录时跳过
    def get_task(self):
        driver = self.driver
        self.pub.comeinifm('right', 'myiframe0')
        trs = driver.find_elements_by_tag_name('tr')
        self.logstu.debug("长度:")
        self.logstu.debug(len(trs))
        driver.switch_to_default_content()
        if len(trs) < 3:
            self.pub.comeinifm('right')
            time.sleep(1)
            self.pub.table_BtnClick(u'获取任务')
            self.logstu.debug(self.pub.is_alert_and_close_and_get_text())
            if self.pub.is_alert_and_close_and_get_text() == u'没有可以获得的任务！':
                raise
            time.sleep(1)
            driver.switch_to_default_content()
            self.pub.leftMenuVagueClick(u'当前工作>当前待办任务', 'left')
        else:self.logstu.debug(u'当前存在任务')

    #提取预期结果字段值
    def get_testcaseValue(self,num,):
        driver = self.driver
        num = self.pub.all_type_to_unicode(num)
        self.dict_data['预期结果'].split('|')[0]


    # 获取当前流程字段的值
    def get_flow(self):
        driver = self.driver
        self.pub.logstu.debug(driver.find_element(*self.current_process).get_attribute('value'))



#########判断是否存在在途数据，如果有，执行，如果无，跳过
    def get_flow1(self):
        driver = self.driver
        #Value1 = self.pub.all_type_to_unicode(Value1)
        text = self.get_Text1()
        self.logstu.debug(u'========= 在途数据审批流程开始 =============')
        for i in range(0,15):
            text1 = self.get_Text1()
            self.logstu.debug(u'在途数据1111111111'+text1)
            #if driver.switch_to_alert():
                #self.logstu.debug(self.close_alert_and_get_its_text())
                #self.close_alert_and_get_its_text()
            if text1 == u'NCIIC照片核查':
                self.Data_in_transit(u'照片符合')
            elif text1 == u'打其他联系人电话':
                self.Data_in_transit(u'信息验证成功')
            elif text1 == u'打父母电话':
                self.Data_in_transit(u'信息验证成功')
            elif text1 == u'办公电话号码核查':
                self.Data_in_transit(u'名称与地址一致')
            elif text1 == u'打办公电话':
                self.Data_in_transit(u'信息验证成功')
            elif text1 == u'打客户移动电话':
                self.Data_in_transit(u'信息验证成功')
            elif text1 == u'主观判断核查':
                self.Data_in_transit(u'AJ1')
                break
            elif text1 == u'百度办公室电话':
                self.Data_in_transit(u'信息验证成功')
            elif text1 == u'支付宝手机查询':
                self.Data_in_transit(u'信息匹配')
            elif text1 == u'支付宝本人手机查询':
                self.Data_in_transit(u'信息匹配')
            elif text1 == u'CE专家审核':
                self.CE_Approver('02','1','testtest')
                break
        self.logstu.debug(u'完成====================')
        self.logstu.debug(self.close_alert_and_get_its_text())
        self.close_alert_and_get_its_text()
        self.logstu.debug(u'========= 在途数据审批流程结束 =============')

    ### 参数 Value1 为当前流程字段的值
    ############ 新任务审批流程
    def get_flow2(self,Value1):
        driver = self.driver
        self.logstu.debug(u'========= 新任务审批流程开始 =============')
        Value1 = self.pub.all_type_to_unicode(Value1)
        text = self.get_Text1()
        if Value1 == (u'bib流程'):

            ##########  NCIIC核查##############
            if text == (u'NCIIC手动身份核查'):
                for count in range(15, 17):
                    strcount = '输入值' + str(count)
                    opinion = self.dict_data[strcount].split('|')[2]
                    remark = self.dict_data[strcount].split('|')[4]
                    self.choose_opinions_Set_remarks(opinion, remark)
                    time.sleep(1)
                    self.pub.logstu.debug(u'【当前流程：bib流程-->流程阶段为：】' + self.get_Text1())
                    self.Next_CheckBtnClick()
                self.baidu_officetel_check()
            if text ==(u'百度办公室电话'):
                self.baidu_officetel_check()
                result = self.dict_data['输入值26'].split('|')[2]
                rownum = self.dict_data['输入值26'].split('|')[4]
                remarks = self.dict_data['输入值26'].split('|')[6]
                self.CE_Approver(result, rownum, remarks)

        if Value1 <> (u'bib流程'):
            if text == (u'NCIIC手动身份核查'):
                ##########  NCIIC核查##############
                for count in range(15, 17):
                    strcount = '输入值' + str(count)
                    opinion = self.dict_data[strcount].split('|')[2]
                    remark = self.dict_data[strcount].split('|')[4]
                    self.choose_opinions_Set_remarks(opinion, remark)
                    time.sleep(1)
                    self.pub.logstu.debug(u'【当前流程：' +Value1 +u'-->流程阶段为：】' + self.get_Text1())
                    self.Next_CheckBtnClick()
                ###########根据Value1 流程阶段执行
                self.doprocess(Value1)
            elif text == (u'文件检查'):
                ######### 文件检查
                self.file_check()
                time.sleep(3)
                ###############################文件检查后点击进一步验证按钮
                #############填写备注
                self.pub.comeinifm('right', 'rightdown', 'frameright', 'myiframe0')
                self.set_remarks(self.dict_data['输入值14'].split('|')[2])
                driver.switch_to_default_content()
                # 点击进一步验证按钮
                time.sleep(1)
                self.Next_CheckBtnClick()
                time.sleep(1)
                if text == u'NCIIC手动身份核查':
                    ##########  NCIIC核查##############
                    for count in range(15, 17):
                        strcount = '输入值' + str(count)
                        opinion = self.dict_data[strcount].split('|')[2]
                        remark = self.dict_data[strcount].split('|')[4]
                        self.choose_opinions_Set_remarks(opinion, remark)
                        time.sleep(1)
                        self.pub.logstu.debug(u'【当前流程：' +Value1 +u'-->流程阶段为：】' + self.get_Text1())
                        self.Next_CheckBtnClick()
                    ###########根据Value1 流程阶段执行
                    self.doprocess(Value1)
                if text <> u'NCIIC手动身份核查':
                    ###########根据Value1 流程阶段执行
                    self.doprocess(Value1)

        self.logstu.debug(u'========= 新任务审批流程结束 =============')




    def doprocess(self,Value1):
        driver = self.driver
        Value1 = self.pub.all_type_to_unicode(Value1)
        if Value1 == (u'judgment流程'):
         ###########2 步验证###########
             self.process_select(Value1, 21)
        if Value1 == (u'easy流程'):
            ###########4 步验证###########
            self.process_select(Value1, 19)
        if Value1 == (u'medium流程'):
            ###########5 步验证###########
            self.process_select(Value1, 18)
        if Value1 == (u'hard流程'):
            ###########6 步验证###########
            self.process_select(Value1, 17)
        if Value1 == (u'student流程'):
            ############ 3步验证########
            ####打父母电话
            self.fumu_tel_check()
            ###执行后续阶段
            self.process_select(Value1,21)
        if Value1 == (u'xcl流程'):
            ############ 3步验证########
            ####打父母电话
            self.fumu_tel_check()
            ###执行后续阶段
            self.process_select(Value1,21)

    #######从意见详情数据 判断 主观判断阶段完成后是否存在后续的 百度办公室电话，支付宝本人手机查询，CE专家审核
    ###参数 Number 该流程的起始阶段名称对应的testcase的输入值的序列号
    def process_select(self,Value,Number):
        driver = self.driver
        Value = self.pub.all_type_to_unicode(Value)
        for count1 in range(Number,23):
            strcount1 = '输入值' + str(count1)
            opinion = self.dict_data[strcount1].split('|')[2]
            remark = self.dict_data[strcount1].split('|')[4]
            self.choose_opinions_Set_remarks(opinion, remark)
            time.sleep(1)
            self.pub.logstu.debug(u'【当前流程：】'+ Value + u'-->流程阶段为：】' + self.get_Text1())
            self.Next_CheckBtnClick()

            #result = self.dict_data['输入值26'].split('|')[2]
            #rownum = self.dict_data['输入值26'].split('|')[4]
            #remarks = self.dict_data['输入值26'].split('|')[6]
            #self.CE_Approver(result,rownum,remarks)
    def fumu_tel_check(self):
        driver = self.driver
        text = self.get_Text1()
        opinion = self.dict_data['输入值18'].split('|')[2]
        remark = self.dict_data['输入值18'].split('|')[4]
        self.choose_opinions_Set_remarks(opinion, remark)
        self.pub.logstu.debug(u'【当前流程：student流程--->流程阶段为：】' + text)
        self.Next_CheckBtnClick()

    def baidu_officetel_check(self):
        driver = self.driver
        for count in range(23, 26):
            text = self.get_Text1()
            strcount = '输入值' + str(count)
            opinion = self.dict_data[strcount].split('|')[2]
            remark = self.dict_data[strcount].split('|')[4]
            self.choose_opinions_Set_remarks(opinion, remark)
            self.pub.logstu.debug('testtesttesttesttesttest')
            self.pub.logstu.debug(u'【当前流程：BIB流程--->流程阶段为：】' + text)
            self.Next_CheckBtnClick()




    def Data_in_transit(self,opinions):
        driver = self.driver
        text = self.get_Text1()
        opinions = self.pub.all_type_to_unicode(opinions)
        self.choose_opinions_Set_remarks(opinions, 'test')
        self.pub.logstu.debug(u'【在途数据-->' + text + u'】')
        self.Next_CheckBtnClick()
        self.pub.is_alert_and_close_and_get_text()

     #####文件检查  input.get_attribute('value') == ('1')  合格
    def file_check(self):
        driver = self.driver
        self.pub.comeinifm('right', 'rightdown', 'frameright')
        self.pub.thread_btn(u'文件检查')
        driver.switch_to_default_content()
        self.pub.goNameWindow(u'小牛消费金融业务管理系统')
        self.pub.comeinifm('ObjectList', 'frameright', 'myiframe0')
        for count in range(1, 14):
            strcount = '输入值' + str(count)
            str_in = self.dict_data[strcount].split('|')[2]
            tds = driver.find_elements(*self.pub.table_tr)[count + 1].find_elements_by_tag_name('td')
            inputs = driver.find_elements(*self.pub.table_tr)[count + 1].find_elements_by_tag_name('input')
            checkname = tds[1].find_element_by_tag_name('input').get_attribute('value')
            for input in inputs:
                if input.get_attribute('type') == ('radio') and input.get_attribute('value') == (str_in):
                    try:
                        input.click()
                        self.logstu.debug(u"文件检查--->检查项" + checkname + u"检查结果--->" + str_in)
                        time.sleep(1)
                    except TimeoutException as e:
                        self.logstu.error(e)


        driver.switch_to_default_content()
        self.pub.comeinifm('ObjectList', 'frameright')
        time.sleep(3)
        self.pub.thread_btn(u'保存')
        self.pub.winClose()

    #进一步验证################ 意见选择######备注##########
    def choose_opinions_Set_remarks(self,opinions,remarks):
        driver = self.driver
        opinions = self.pub.all_type_to_unicode(opinions)
        remarks = self.pub.all_type_to_unicode(remarks)
        time.sleep(1)
        self.pub.comeinifm('right', 'rightdown', 'frameright', 'myiframe0')
        Number = len(driver.find_elements_by_tag_name('tr'))
        self.pub.logstu.debug('行数:'+str(Number))

        trs = driver.find_elements_by_tag_name('tr')
        tds = trs[1].find_elements_by_tag_name('td')
        td_text = tds[1].text
        self.pub.logstu.debug(td_text)
        value = tds[1].text.split('\n')
        if Number == 3:
            ########选择意见
            for js in range(len(value)):
                if opinions == value[js]:
                    trs[1].find_elements_by_tag_name('input')[js].click()
                    self.logstu.debug(u'【流程阶段为：】' + self.get_Text1() +u"意见详情--->" + value[js])
                    time.sleep(3)
                    break
            ###填写 备注 remarks
            time.sleep(1)
            for i in range(0,5):
                try:
                    if trs[Number-1].find_element_by_tag_name('textarea'):
                        trs[Number - 1].find_element_by_tag_name('textarea').clear()
                        trs[Number - 1].find_element_by_tag_name('textarea').send_keys(remarks)
                        break
                except StaleElementReferenceException as e:
                    self.logstu.error(e)
            time.sleep(1)
            driver.switch_to_default_content()
        if Number >3:
            ########选择意见
            for js in range(len(value)):
                if opinions == value[js]:
                    trs[1].find_elements_by_tag_name('input')[js].click()
                    self.logstu.debug(u'【流程阶段为：】' + self.get_Text1() +u"意见详情:" + value[js])

                    break
            ###填写 备注 remarks
            time.sleep(1)
            for i in range(0, 5):
                try:
                    if trs[Number - 1].find_element_by_tag_name('textarea'):
                        trs[Number - 1].find_element_by_tag_name('textarea').clear()
                        trs[Number - 1].find_element_by_tag_name('textarea').send_keys(remarks)
                        break
                except StaleElementReferenceException as e:
                    self.logstu.error(e)
            driver.switch_to_default_content()

    def suggestion_choose(self,value):
        driver = self.driver
        value = self.pub.all_type_to_unicode(value)
        self.pub.comeinifm('right', 'rightdown', 'frameright', 'myiframe0')
        time.sleep(3)
        trs = driver.find_elements_by_tag_name('tr')
        inputs = trs[1].find_elements_by_tag_name('input')[int(value)].click()
    ###填写 备注 remarks
    def set_remarks(self,remarks):
        driver = self.driver
        remarks = self.pub.all_type_to_unicode(remarks)
        self.pub.logstu.debug(len(driver.find_elements_by_tag_name('tr')))
        Number = len(driver.find_elements_by_tag_name('tr'))
        trs = driver.find_elements_by_tag_name('tr')
        time.sleep(3)
        ###填写 备注 remarks
        time.sleep(1)
        trs[1].find_element_by_tag_name('textarea').clear()
        trs[1].find_element_by_tag_name('textarea').send_keys(remarks)
        driver.switch_to_default_content()


    def set_remarks2(self,remarks):
        driver = self.driver
        time.sleep(3)
        trs = driver.find_elements_by_tag_name('tr')
        ###填写 备注 remarks
        time.sleep(1)
        trs[3].find_element_by_tag_name('textarea').clear()
        trs[3].find_element_by_tag_name('textarea').send_keys(remarks)
        driver.switch_to_default_content()


    def Next_CheckBtnClick(self):
        driver = self.driver
        self.pub.comeinifm('right', 'rightdown', 'frameright')
        self.pub.thread_btn(u'进一步验证')
        driver.switch_to_default_content()

    def Next_CheckBtnClick2(self):
        driver = self.driver
        self.pub.comeinifm('right', 'rightdown', 'frameright')
        self.pub.thread_btn(u'进一步验证')
        if driver.switch_to_alert():
            self.logstu.debug(self.close_alert_and_get_its_text())
            self.close_alert_and_get_its_text()
            try:
                driver.switch_to_default_content()
            except UnexpectedAlertPresentException as e:
                self.logstu.error(e)
                self.logstu.error('11111111')
        else:driver.switch_to_default_content()




    ##############获取阶段名称
    def get_Text1(self):
        driver = self.driver
        time.sleep(1)
        self.pub.comeinifm('right', 'rightup', 'frameright')
        d_text = driver.find_element_by_tag_name('b').text
        self.logstu.debug(u'当前阶段名称：' + d_text)
        driver.switch_to_default_content()
        return d_text

    ########获取number,
    def get_num(self):
        driver = self.driver
        text = self.get_Text1()
        self.logstu.debug(u'对应文本信息:' +text)
        for num in range(14,25):
            str_in = '输入值' + str(num)
            self.logstu.debug(self.dict_data[str_in].split('|')[0])
            if text == self.dict_data[str_in].split('|')[0]:
                self.logstu.debug(u'当前对应testcase中的输入值'+str(num))
                return num

############新增 2016-07-06

    def CE_Approver(self, result, rownum, remarks):
        driver = self.driver
        text = self.get_Text1()
        rownum = int(rownum)
        result = self.pub.all_type_to_unicode(result)
        remarks = self.pub.all_type_to_unicode(remarks)
        time.sleep(1)
        self.pub.comeinifm('right', 'rightdown', 'frameright', 'myiframe0')
        Number = len(driver.find_elements_by_tag_name('tr'))
        self.pub.logstu.debug('行数:' + str(Number))
        trs = driver.find_elements_by_tag_name('tr')
        tds = trs[1].find_elements_by_tag_name('td')
        inputs = tds[1].find_elements_by_tag_name('input')
        if Number == 6:
            ####审核结果
            for input in inputs:
                self.logstu.debug('3333333333')
                self.logstu.debug(input)
                self.logstu.debug(result)
                if (result == input.get_attribute('value') == '01') and input.get_attribute('type') == 'radio':
                    self.logstu.debug(input)
                    input.click()
                    self.logstu.debug(u'审核结果:' + input.get_attribute('value'))
                    self.logstu.debug('222222222222222222222222222222222')
                    selectinput = trs[2].find_elements_by_tag_name('input')[1]
                    self.pub.thread_btn2(selectinput)
                    driver.set_page_load_timeout(2)
                    self.pub.comeinifm('ObjectList', 'myiframe0')
                    driver.find_elements(*self.pub.table_tr)[rownum + 1].click()
                    inputs1 = driver.find_elements(*self.pub.table_tr)[rownum + 1].find_elements_by_tag_name('input')
                    text = inputs1[1].get_attribute('value')
                    driver.switch_to_default_content()
                    self.logstu.debug(u'拒绝原因:' + text)
                    self.pub.thread_btn2(driver.find_element(*self.Confirm))
                    self.logstu.debug('33333333333333333333333333333333')
                    self.pub.comeinifm('right', 'rightdown', 'frameright', 'myiframe0')
                    trs[3].find_element_by_tag_name('textarea').clear()
                    trs[3].find_element_by_tag_name('textarea').send_keys(remarks)
                    driver.switch_to_default_content()
                    self.pub.logstu.debug(u'【CE审核 -- >流程阶段为：】' + text)
                    self.Next_CheckBtnClick2()
                    break

                if (result == input.get_attribute('value') == ('02' or '03')) and input.get_attribute('type') == 'radio':
                    self.logstu.debug(input)
                    input.click()
                    self.logstu.debug(u'审核结果:' + input.get_attribute('value'))
                    #trs[2].find_elements_by_tag_name('input')[1].click()
                    trs[3].find_element_by_tag_name('textarea').clear()
                    trs[3].find_element_by_tag_name('textarea').send_keys(remarks)
                    self.logstu.debug('111111111111111111111111111111')
                    driver.switch_to_default_content()
                    self.pub.logstu.debug(u'【CE审核 -- >流程阶段为：】' + text)
                    self.Next_CheckBtnClick2()
                    break

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.driver.switch_to_alert():
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        except NoAlertPresentException as e:
            self.logstu.debug(e)
        finally: pass

        ############新增 2016-07-12
        #####获取两个关键字段
        ############获取当前流程字段值，便于后续使用########################
    def get_Value(self):
        driver = self.driver
        self.pub.comeinifm('right', 'myiframe0')
        Value = driver.find_element(*self.current_process).get_attribute('value')
        self.pub.logstu.debug(Value)
        # self.comm.write_file(Value1,self.row,self.get_key_cell_col("执行结果"))
        self.pub.logstu.error('进件申请编号:')
        self.pub.logstu.error(driver.find_element(*self.Contract_Num).get_attribute('value'))
        # 选中列表第一行记录
        self.pub.table_RowClick(-2)
        driver.switch_to_default_content()
        self.pub.comeinifm('right')
        self.pub.table_BtnClick(u'签署意见')
        driver.switch_to_default_content()
        return Value