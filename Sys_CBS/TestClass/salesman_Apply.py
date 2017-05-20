# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from Sys_CBS.PageObj.lyElementsOperation import PublicAct
from Sys_CBS.PageObj.jFunction import Function
from Sys_CBS.PageObj.salesmanFunction import SalesmanFunction
import unittest, time, re, sys, os,xlwt,xlrd,urllib2
from xlutils.copy import copy
from Utils.RandomShenFenZhen import RandomShenFen
reload(sys)
sys.setdefaultencoding('utf-8')

class SalesmanApply(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row =""          #接收main脚本传送的当前处理的行数
    ####身份证号码 --- 查询条件
    select_identitycard = (By.CSS_SELECTOR,"input[id=\"DF3_1_INPUT\"]")
    #######列表中的身份证号码字段
    table_identitycard = (By.CSS_SELECTOR, "input[name=\"R0F4\"]")
    #table_identitycard =  (By.XPATH,"//html/body/form/div/table/tbody/tr[3]/td[5]/input")

    def setUp(self):
        #self.driver = self.comm.get_browserdrvie('Chrome')
        self.driver = self.mainWebDr
        self.driver.implicitly_wait(30)
        self.salesman = SalesmanFunction(self.driver)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.execldata = ""
        self.filepath = ""
        #self.driver = self.Login(self.dict_data["登录用户"],self.dict_data["登录密码"])
        self.pub = PublicAct(self.driver)
        self.RShenFenZhen = RandomShenFen()
        #self.Fun = Function()

        #进入具体菜单
        self.driver.implicitly_wait(6)
        #self.comm.goto_menu(self.driver,self.row)
        self.pub.goto_menu(self.dict_data)
        print self.row

    def test_SalesmanApply(self):
        if self.dict_data["操作类型"].encode('utf8') == 'Excel导入':
            self.pub.logstu.info('Excel导入')
            self.excelimport()
        if self.dict_data["操作类型"].encode('utf8') == '导入申请':
            self.pub.logstu.info('导入申请')
            self.Apply()
        if self.dict_data["操作类型"].encode('utf8') == '重新申请':
            self.logstu.info(u"重新申请")
            self.re_operation()
        if self.dict_data["操作类型"].encode('utf8') == 'Excel导出':
            self.logstu.info(u"Excel导出")
            self.down_load()

    def excelimport(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.thread_btn('Excel导入')
        for i in range(0,6):
            ###更新导入模板的测试数据
            Data = self.get_identitycardnumber2()
            self.pub.logstu.debug('Data:'+Data)


            # 从selenium获取cookie， 和url从中提取aoID
            cookise = driver.get_cookies()
            self.logstu.debug(cookise)
            icookise = ''
            for cook in cookise:
                if icookise != '':
                    icookise = icookise + ';'
                icookise = icookise + '%s=%s' % (cook['name'], cook['value'])
            self.logstu.debug(icookise)
            self.logstu.debug(driver.current_url)
            selenium_aoid = driver.current_url.split('aoID=')[1]

            myhttp = IHttpAct()
            myhttp.iCookie = icookise
            ip = self.dict_data["登录地址"].split('/')[2]
            self.pub.logstu.debug('ip地址：'+ip)

            newaoID_url = 'http://'+ip+'/XiaoNiu/Redirector?OpenerClientID='+ \
                          selenium_aoid + '&ComponentURL=/BusinessManage/StoreManage/FileSelectForDataImport.jsp'
            # 发起get请求，该地址获取上传文件请求所需的aoID值以及cookie，包含一次Location跳转
            getaoid = myhttp.get_http_request(newaoID_url)
            #self.logstu.debug(getaoid)
            self.logstu.debug('获取最新的上传文件aoID：%s' % (myhttp.i_aoID))
            self.logstu.debug('------------upload File Start------------')
            # 获取文件上传二进制数据
            #excel_path = sys.path[0] + os.sep + r'data' + os.sep + r'salesman.xls'
            excel_path = r'data/salesman.xls' #salesman.xls
            self.logstu.debug(excel_path)
            # 拼装post文件及其它数据
            data = {'CompClientID': myhttp.i_aoID, # 获取自动更新的aoID
                    'DocNo': '', #null
                    'FileName': 'salesman.xls'}
            #myhttp.myhead['Content-Type'] = 'multipart/form-data;' # 设置上传文件的head
            myhttp.myhead['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C)'
            upfilerul = myhttp.upfile_requests(
                'http://'+ip+'/XiaoNiu/AppConfig/Document/AttachmentUpload2.jsp?CompClientID='
                + myhttp.i_aoID, data, excel_path)
            self.logstu.debug(upfilerul)
            self.assertNotEqual(None, re.search(r'(?<=self.returnValue=").*?(?=";)', upfilerul, re.M | re.I),'未找到返回值')
            msg_url_p = re.search(r'(?<=self.returnValue=").*?(?=";)', upfilerul, re.M | re.I).group()
            self.logstu.debug(msg_url_p)

            msg_url_userid = ''
            if re.search(r'(?<=UserID=).*?(?=;)', myhttp.iCookie, re.M | re.I) != None:
                msg_url_userid = re.search(r'(?<=UserID=).*?(?=;)', myhttp.iCookie, re.M | re.I).group()
            elif re.search(r'(?<=UserID=).*?(?=$)', myhttp.iCookie, re.M | re.I) != None:
                msg_url_userid = re.search(r'(?<=UserID=).*?(?=;)', myhttp.iCookie, re.M | re.I).group()
            self.assertNotEqual('', msg_url_userid, '未找到Cookie值UserID')
            msg_url_userid = re.search(r'(?<=UserID=).*?(?=;)', myhttp.iCookie, re.M | re.I).group()
            self.logstu.debug(msg_url_userid)
            orgid = msg_url_userid[0:msg_url_userid.find('0')]
            self.logstu.debug(orgid)

            myhttp.myhead['X-Requested-With'] = 'XMLHttpRequest'
            del myhttp.myhead['Content-Type']
            myhttp.get_http_request('http://'+ip+'/XiaoNiu/Frame/page/control/'
                                    'DestroyCompAction.jsp?ToDestroyClientID=' + myhttp.i_aoID)
            self.logstu.debug(myhttp.myhead)
            for i in range(0, 10):
                time.sleep(1)
                up_message = myhttp.get_http_request('http://'+ip+'/XiaoNiu/servlet/run?'
                                                 'ClassName=com.amarsoft.app.proj.ExcelDataImport&'
                                                 'MethodName=importSalesmanInfomation&Args=filePath='
                                                 + msg_url_p + ',userid='+ msg_url_userid
                                                 + ',orgid='+ orgid + '&ArgsObject=Sqlca')
                if up_message.find('AWES0009') == -1:
                    break
                break
                time.sleep(1)
            self.logstu.debug('------------upload File End------------')
            self.pub.logstu.debug('11111111111111111111111111111')
            self.pub.logstu.debug(up_message)
            #if up_message.find(u'在系统中已经存在') != -1:
                #raise Exception(up_message)

        ###################################################################
        ###关闭弹窗
        self.pub.winClose2()
        ########查询数据是否导入成功，并将身份证号码写入执行结果，后续使用
        self.pub.comeinifm('right')
        driver.find_element(*self.select_identitycard).send_keys(Data)
        self.pub.select_btn(u'查询')
        driver.switch_to_default_content()
        self.pub.comeinifm('right','myiframe0')
        Value = driver.find_element(*self.table_identitycard).get_attribute('value')
        self.pub.logstu.debug('列表中的身份证号码：'+Value)

        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                    % (self.actdb.casetitle_cn['执行结果'], Value, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)
        self.assertEqual(Data,Value)



    def Apply(self):
        driver = self.driver
        current_handle = driver.current_window_handle
        self.pub.comeinifm('right')
        driver.find_element(*self.select_identitycard).send_keys(self.dict_data['查询条件1'].split('|')[1])
        self.pub.select_btn(u'查询')
        self.pub.comeinifm('right','myiframe0')
        driver.find_element(*self.table_identitycard).click()
        time.sleep(3)
        driver.switch_to_default_content()
        self.salesman.BtnClick(u'申请详情')
        self.pub.goNameWindow(u'小牛消费金融业务管理系统')
        self.pub.comeinifm('ObjectList','DeskTopInfo','right','myiframe0')
        driver.execute_script("document.getElementById('R0F20').readOnly = true;")
        driver.switch_to_default_content()

        self.pub.setEditTableValues(self.dict_data, 'ObjectList','DeskTopInfo', 'right', 'myiframe0')

        #str_in = driver.find_element_by_id('R0F4').get_attribute('value')  ##身份证号
        #self.comm.write_file(str_in,self.row,self.comm.get_key_cell_col("执行结果"))
        #保存，关闭弹框并切换到旧窗口
        self.pub.comeinifm("ObjectList","DeskTopInfo","right")
        self.pub.thread_btn(u'保存')
        driver.implicitly_wait(10)
        self.pub.winClose2()
        for i in range(0,3):
            try:
                driver.switch_to_window(current_handle)
                break
            except :self.pub.logstu.debug('raise ResponseNotReady()')

        self.pub.logstu.debug(driver.title)
        #点击提交按钮，并且判断是否提交成功
        #判断用例是否执行成功
        #rul = self.salesman.getAlertText()
        self.assertNotEqual(self.getAlertText(), -1)
        #rul = self.getAlertText()
        #self.pub.logstu.debug(rul)
        #self.assertEqual(rul,self.pub.all_type_to_encode(self.dict_data['预期结果']))



    #add by limeng
    def re_operation(self):
        driver = self.driver
        #读取省份证号码
        cert_id = self.dict_data["查询条件1"].split("|")[1]
        #cert_id = "44010019850602504X"
        self.pub.comeinifm('left')
        self.pub.click_btn(driver.find_element_by_css_selector("a[title='审批再次申请'][id='text3']"))
        time.sleep(1)
        self.pub.comeinifm('right', 'myiframe0')
        self.pub.click_btn(driver.find_element_by_css_selector("input[value='%s']" % cert_id))
        #进入申请详情，点击保存
        self.pub.comeinifm('right')
        self.pub.thread_btn("申请详情")
        time.sleep(1)
        self.pub.comeinifm('ObjectList', 'DeskTopInfo', 'right')
        self.pub.table_BtnClick_NoSetTimeOut('保存')
        self.pub.winClose()
        time.sleep(1)
        #重新提交申请
        self.pub.comeinifm('right')
        self.pub.table_BtnClick_NoSetTimeOut("提交")
        self.pub.is_alert_and_close_and_get_text()
        time.sleep(5)
    #add by limeng
    def down_load(self):
        driver = self.driver
        #确定导出哪个模块
        content = self.dict_data["查询条件1"]
        self.pub.comeinifm('left')
        self.pub.click_btn(driver.find_element_by_css_selector("a.pt9song[title='%s']" % content))
        time.sleep(1)
        #点击Excel导出，火狐浏览器实际上不能这么操作
        self.pub.comeinifm('right')
        try:
            self.pub.thread_btn('Excel导出')
        except Exception as e:
            self.logstu.info(e)
        time.sleep(2)
        #采用调用接口的方式进行Excel导出,优先级比较低，暂时搁置

        url = "http://10.20.2.12:7001/XiaoNiu/Resources/1/Support/GetDWDataAll.jsp?" \
              "CompClientID=C2016071314583401061003158104265&type=export&" \
              "dw=SalesmanApplyList_P20160713145834026463734817344&rand=7386745153654181"
        url1 = "http://10.20.2.12:7001/XiaoNiu/servlet/view/file"
        f = urllib2.urlopen(url)
        data = f.read()
        self.logstu.info(data)
        self.logstu.info('1111111111111111111111111111111111111111')
        with open("demo2.zip", "wb") as code:
            code.write(data)
			
		#提交

    def getAlertText(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.logstu.error('6666666666666666666666666666666')
        self.pub.logstu.error(self.pub.thread_btn(u'提交'))
        Result2 = driver.switch_to_alert().text.strip(u"！").find(u'提交成功')
        self.pub.logstu.error('77777777777777777777777')
        self.pub.logstu.error(Result2)
        if Result2 == 0:
            self.pub.logstu.error('Result2 == 0')
            return self.pub.is_alert_and_close_and_get_text()
            '''
            try:driver.switch_to_alert().accept()
            except NoAlertPresentException as e:self.pub.logstu.debug(e)
            return Result2'''
        elif Result2 == -1:
            self.pub.logstu.error('Result2 == -1')
            # return self.pub.is_alert_and_close_and_get_text()
            try:
                alert11 = driver.switch_to_alert()
                self.pub.logstu.cri(alert11.text)
                alert11.accept()
            except NoAlertPresentException as e:
                self.pub.logstu.debug(e)
            self.pub.logstu.debug(u'开始操作第二个alert window')
            Alert1 = driver.switch_to_alert()
            self.pub.logstu.cri(Alert1.text)
            Result3 = Alert1.text.strip(u"！").find(u'提交成功')
            try:
                self.pub.logstu.debug(u'Alert1.text:\n\t' + Alert1.text)
                Alert1.accept()
            except NoAlertPresentException as e:
                self.pub.logstu.debug(e)
            return Result3

    def getAlertText1(self):
        driver = self.driver
        self.pub.comeinifm('right')
        self.pub.logstu.error(self.pub.thread_btn(u'提交'))
        try:
            Result2 =driver.switch_to_alert().text.strip(u"！").find(u'提交成功')
        except NoAlertPresentException as e:
            self.pub.logstu.debug(e)
        self.pub.logstu.error(Result2)
        if  Result2 == 0:
            self.pub.logstu.error('Result2 == 0')
            return self.pub.is_alert_and_close_and_get_text()
            '''
            try:driver.switch_to_alert().accept()
            except NoAlertPresentException as e:self.pub.logstu.debug(e)
            return Result2'''
        elif Result2 == -1:
            self.pub.logstu.error('Result2 == -1')
            return self.pub.is_alert_and_close_and_get_text()
            '''
            try:driver.switch_to_alert().accept()
            except NoAlertPresentException as e:print e
            driver.implicitly_wait(5)
            Alert1 = driver.switch_to_alert()
            Result3 = Alert1.text.strip(u"！").find(u'提交成功')
            try:
                self.pub.logstu.debug(u'Alert1.text:\n\t' + Alert1.text)
                Alert1.accept()
            except NoAlertPresentException as e:print e
            return Result3
            '''











    '''

    def Login(self,Uname,Password):
        self.driver.quit()
        driver = webdriver.Ie()
        #IE登录系统
        #Uname = self.dict_data["登录用户"]
        #Password = self.dict_data["登录密码"]
        username = self.salesman.all_type_to_unicode(Uname)
        password = self.salesman.all_type_to_unicode(Password)
        print username,password
        driver.get(self.dict_data["登录地址"])
        driver.find_element_by_xpath("//input[@name='UserID']").clear()
        driver.find_element_by_xpath("//input[@name='UserID']").send_keys(username)
        driver.find_element_by_xpath("//input[@name='Password']").clear()
        driver.find_element_by_xpath("//input[@name='Password']").send_keys(password)
        time.sleep(3)
        driver.find_element_by_xpath("//input[@class='button_submit' and @onclick='doSubmit()']").click()

        if driver.switch_to_alert():
            try:driver.switch_to_alert().accept()
            except NoAlertPresentException as e: print 'NoAlertPresentException: login switch_to_alert'
        return driver

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    '''

############从文本文件中取一行数据，并写入excel中
    def get_identitycardnumber(self):

        ###从记事本中提取一行，并在记事本中删除该行
        #path = sys.path[0] + "\\data\\testcase.xls"
        path = sys.path[0] + "\\data\\identitycardnumber.txt"
        textfile = open(path, 'r')
        All_data = textfile.read()
        self.pub.logstu.debug(u'剩余行数：' + str(len(All_data.split('\n'))))
        # print '行数：',len(textfile.readlines())
        ##第一行数据
        data = All_data.split('\n')[0]
        self.pub.logstu.debug( u'从记事本中提取的身份证号码：'+data)
        ##去掉第一行空行
        newdata = All_data.strip(data).strip()
        self.pub.logstu.debug(u'剩余行数：'+str(len(newdata.split('\n'))))
        textfile.close()
        textfile2 = open(path, 'w')
        textfile2.write(newdata)
        textfile2.close()
        ##将记事本中的提取出来的数据写入excel文件
        excelfilepath = sys.path[0] + '\\data\\salesman.xls'
        excelworkbook = xlrd.open_workbook(excelfilepath)
        sheet = excelworkbook.sheet_by_name('sheet1')
        print 'sheet:', sheet
        newworkbook = copy(excelworkbook)
        newworkbook_sheet = newworkbook.get_sheet(0)
        newworkbook_sheet.write(1, 2, data)
        newworkbook.save(excelfilepath)
        return data

    def get_identitycardnumber2(self):

        data = self.RShenFenZhen.makeNew()
        #data = '371501198509204714'
        self.pub.logstu.debug('Data:' + data)
        ##将记事本中的提取出来的数据写入excel文件
        excelfilepath = sys.path[0] + '\\data\\salesman.xls'
        excelworkbook = xlrd.open_workbook(excelfilepath)
        sheet = excelworkbook.sheet_by_name('sheet1')
        print 'sheet:', sheet
        newworkbook = copy(excelworkbook)
        newworkbook_sheet = newworkbook.get_sheet(0)
        newworkbook_sheet.write(1, 2, data)
        newworkbook.save(excelfilepath)
        return data

