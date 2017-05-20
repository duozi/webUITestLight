# -*- coding: UTF-8 -*-
import unittest,sys,os,time, logging, xmlrunner, datetime,ConfigParser
from Utils.writeReport import CreateHtmlReport
from Utils.UnitTestRultAct import UnitTestRultAct
from Utils.CustTestRult import CustTestRult
#这里需要导入测试文件
from Utils.commFunction import CommFunction
from Utils.logger import Logger
from Utils.testMySqlAct import TestMySqlAct
from Utils.lyFunction import PubFunction
from Utils.scriptTestCase import scriptTestCase

class main_class(object):
    reload(sys)
    sys.setdefaultencoding('utf8')
    s = os.sep
    pubf = PubFunction()
    comm = CommFunction()
    sTC = scriptTestCase()
    caserult = UnitTestRultAct()
    logstu = Logger(sys.path[0] + s + 'logs' + s + 'autotest.log', logging.INFO, logging.DEBUG)  # ERROR
    Screenshotfilepath = pubf.Create_folder_current_path()

    cf = ConfigParser.ConfigParser()
    cf.read('test.conf')
    db_host = cf.get('db', 'host')
    db_port = cf.getint('db', 'port')
    db_name = cf.get('db', 'db')
    db_user = cf.get('db', 'user')
    db_passwd = cf.get('db', 'passwd')
    db_charset = cf.get('db', 'charset')
    runmode = cf.get('run_mode','run_mode')
    IsGetDataFromDB = cf.get('ScriptCaseGetDataFromDB', 'IsGetDataFromDB')
    browserName = cf.get('browser', 'browserName')

    testSys = 'ALL'  # CBS carloan
    testENV = 'ALL'  # 环境默认值 UAT1， 还有stg等
    iTestSuite = []
    browsedrive = comm.get_browserdrvie(browserName)
    actdb = TestMySqlAct(host=db_host, db=db_name, user=db_user, passwd=db_passwd,port=db_port, charset=db_charset)

    def runDBcase(self):
        self.logstu.info(u'运行从数据库中读取的用例')
        # 连接数据库
        # actdb = TestMySqlAct(host=self.db_host, db=self.db_name, user=self.db_user, passwd=self.db_passwd, port=self.db_port, charset=self.db_charset)
        # 把测试用例表testcase的数据更新到执行表
        self.actdb.table = self.actdb.testCaseSel(self.actdb.testcaseSelSql)  # 获取测试用例列表
        self.actdb.table_copy = self.actdb.testCaseSel(self.actdb.testcase_copySelSql)  # 获取测试用例列表
        str1 = ''
        for k in range(0, len(self.actdb.table_copy)):
            if str1 == '':
                str1 = str(self.actdb.table_copy[k]['test_id'])
            else:
                str1 = str1 + ',' + str(self.actdb.table_copy[k]['test_id'])
        chrild_cellstr = str1.split(",")
        for i in range(0, len(self.actdb.table)):
            if str(self.actdb.table[i]['test_id']) in chrild_cellstr:
                for j in range(0, len(self.actdb.table_copy)):
                    if self.actdb.table[i]['test_id'] == self.actdb.table_copy[j]['test_id']:
                        self.actdb.UpdateCaseRecord(i)
                        break
            else:
                print 'testcase: ' + str(self.actdb.table[i]['test_id']) + ' ' + self.actdb.table[i]['case_details']
                self.actdb.insertRecord(i)

        self.actdb.testCaseDel('TRUNCATE webuiruntime')  # 删除临时表数据
        # copy 需要执行的测试用例到临时表
        self.actdb.testCaseUpdate('INSERT INTO webuiruntime SELECT * FROM webuicase')
        self.actdb.table = self.pubf.dict_None_to_Str(self.actdb.testCaseSel(self.actdb.caseselstr))

        alltestnum = len(self.actdb.table)  # 需要执行用例的个数
        # logstu = Logger(sys.path[0] + s + 'logs' + s + 'autotest.log', logging.INFO, logging.DEBUG)  # ERROR
        # 获取菜单对应脚本矩阵
        dict_menu_script = self.comm.get_menu_to_script()
        # 执行脚本对应的脚本类名
        scriptname = ""
        print "start -  -   -"
        # 测试环境设置
        # sonSys = 'CBS' 'NCP'
        sonSys = 'NCP,CBS'
        testENV = 'UAT'  # 环境默认值 uat， 还有stg等
        if len(sys.argv) > 1:
            for i in range(1, len(sys.argv)):
                print "Start Parameter:", i, sys.argv[i]
                if sys.argv[i].find("=") != -1:
                    tmp = sys.argv[i].split('=')
                    if tmp[0].upper() == 'S' or tmp[0].upper() == 'SYS':
                        sonSys = tmp[1]
                    if tmp[0].upper() == 'V' or tmp[0].upper() == 'ENV':
                        testENV = tmp[1]
                else:
                    testENV = sys.argv[1]
                    if i == 2:
                        sonSys = sys.argv[2]

        # 循环读取测试数据
        # iTestSuite = []
        for i in range(0, alltestnum):
            # 运行标志不是 1 的用例不运行测试
            if self.actdb.table[i]['is_run'] != 1:
                self.logstu.debug('运行标识不为 1 的案例跳过：%s -- %s -- %s' % (
                    self.actdb.table[i]['test_order'], self.actdb.table[i]['case_title'], self.actdb.table[i]['case_details']))
                continue
            # 判断测试环境运行测试，排除非指定环境
            if testENV.find(',') == -1:
                if self.actdb.table[i]['environment'].upper() != testENV.upper():
                    continue
            else:
                vflag = False;
                for env in testENV.split(','):
                    if self.actdb.table[i]['environment'].upper() == env.upper():
                        vflag = True;
                if vflag == False:
                    continue
            # 判断子系统
            if sonSys.find(',') == -1:
                if self.actdb.table[i]['subsystem'].upper() != sonSys.upper():
                    continue
            else:
                sflag = False;
                for son in sonSys.split(','):
                    if self.actdb.table[i]['subsystem'].upper() == son.upper():
                        sflag = True;
                if sflag == False:
                    continue;
            try:
                iTestCase = {}
                # 将数据库查询得到的字典的key替换为中文
                dict_row_data = self.pubf.dict_key_update(self.actdb.table[i], self.actdb.casetitle_cn)
                # 对数据中的特殊字段做处理，如rd(10) up(1)等
                dict_row_data = self.actdb.rowdata_update(dict_row_data, i)
                # 获取最后一级的菜单名
                menuname = ''
                if dict_row_data['一级菜单'] != None and dict_row_data['一级菜单'] != '':
                    menuname = self.pubf.all_type_to_encode(dict_row_data['一级菜单']).strip()
                if dict_row_data['二级菜单'] != None and dict_row_data['二级菜单'] != '':
                    menuname = self.pubf.all_type_to_encode(dict_row_data['二级菜单']).strip()
                if dict_row_data['三级菜单'] != None and dict_row_data['三级菜单'] != '':
                    menuname = self.pubf.all_type_to_encode(dict_row_data['三级菜单']).strip()
                self.logstu.debug('当前操作：%s' % menuname)
                print menuname
                # 获取菜单对应的脚本名字和类名
                actObject = self.pubf.all_type_to_encode(dict_row_data['操作对象']).strip()
                dict_menu_script[actObject]
                LoadScriptObject =  dict_menu_script[actObject].split("|")
                module_name = LoadScriptObject[0]  # 需要导入的模块名
                class_name = LoadScriptObject[1]  # 需要导入的类名
                #dict_menu_script[menuname]
                # menutemp = dict_menu_script[menuname].split("|")
                # module_name = menutemp[0]  # 需要导入的模块名
                # class_name = menutemp[1]  # 需要导入的类名
                self.logstu.debug('导入类：%s, class：%s' % (module_name, class_name))
                # 相同用例编号 case_num的用例，前面的失败了，后面的skip跳过测试，避免一个失败引起一堆失败
                if len(self.iTestSuite) > 1:
                    last = len(self.iTestSuite) - 1
                    if self.iTestSuite[last]['errors'] > 0 or self.iTestSuite[last]['failures'] > 0 or self.iTestSuite[last][
                        'skipped'] > 0:
                        previous_step = ''
                        if self.iTestSuite[last]['errors'] > 0 or self.iTestSuite[last]['failures']:
                            previous_step = '上一步测试用例执行失败，当前步骤有依赖关系跳过执行 skipped.'
                        else:
                            previous_step = '上一步测试用例执行 skipped，当前步骤有依赖关系跳过执行 skipped.'
                        if self.iTestSuite[last]['case_num'] == dict_row_data['案例编号']:
                            iTestCase['case_num'] = dict_row_data['案例编号']  # dict_row_data["用例编号"]
                            iTestCase['environment'] = dict_row_data['环境']
                            iTestCase['subsystem'] = dict_row_data['子系统']
                            iTestCase['title'] = dict_row_data["案例名称"]  # dict_row_data["案例名称"]
                            iTestCase['details'] = dict_row_data["案例详情"]  # dict_row_data["案例详情"]
                            iTestCase['run'] = 1
                            iTestCase['successes'] = 0
                            iTestCase['successes_str'] = ''
                            iTestCase['errors'] = 0
                            iTestCase['errors_str'] = ''
                            iTestCase['failures'] = 0
                            iTestCase['failures_str'] = ''
                            iTestCase['skipped'] = 1
                            iTestCase['skipped_str'] = [(module_name + '.' + class_name, previous_step)]
                            iTestCase['img'] = ''
                            iTestCase['start_time'] = self.iTestSuite[last]['stop_time']
                            iTestCase['stop_time'] = time.time()
                            iTestCase['time_consuming'] = iTestCase['stop_time'] - iTestCase['start_time']
                            self.iTestSuite.append(iTestCase)
                            continue

                if (dict_row_data["登录用户"] <> "" and dict_row_data["登录密码"] <> "") and dict_row_data["子系统"] <> "ncp":
                    self.browsedrive.quit()
                    self.browsedrive = self.comm.login_success(dict_row_data["子系统"], dict_row_data["登录地址"], dict_row_data["登录用户"],
                                                     dict_row_data["登录密码"], self.browserName)
                else:
                    self.browsedrive.quit()

                # 动态导入要执行的脚本类
                module = __import__(module_name)
                # 动态导入要执行的脚本对应的类
                exec_class = getattr(module, class_name)
                # 把测试数据传送给执行脚本里的类
                exec_class.mainWebDr = self.browsedrive
                exec_class.comm = self.comm
                exec_class.dict_data = dict_row_data
                exec_class.logstu = self.logstu
                exec_class.actdb = self.actdb
                exec_class.row = i
                exec_class.Screenshotfilepath = self.Screenshotfilepath
                testunit = unittest.TestSuite()
                # 将测试用例加入到测试容器(套件)中
                testunit.addTest(unittest.makeSuite(exec_class))
                # 执行测试套件,失败重测，最多重复3次，最后一次或者成功的那一次写入测试结果中
                for j in range(0, 2):
                    testRunner = xmlrunner.XMLTestRunner(output=sys.path[0] + self.s + 'output')  # ,outsuffix='wow2'
                    testRunner.failfast = False
                    testRunner.buffer = False
                    testRunner.catchbreak = False
                    var = testRunner.run(testunit)
                    if len(var.errors) == 0 and len(var.failures) == 0:
                        self.logstu.info('Main Message:\n案例 %s|%s|%s 测试通过' % (dict_row_data["案例编号"],dict_row_data["案例名称"],dict_row_data["案例详情"]))
                        break
                    else:
                        self.logstu.info('Main Message:\n案例 %s|%s|%s 测试未通过' % (dict_row_data["案例编号"],dict_row_data["案例名称"],dict_row_data["案例详情"]))
                        continue
                    for fail in var.failures:
                        self.logstu.error('fail function: %s' % fail[0].test_id)
                        self.logstu.error('fail message: %s' % fail[1])
                    for error in var.errors:
                        self.logstu.error('error function: %s' % error[0].test_id)
                        self.logstu.error('error message: %s' % error[1])

                imgpath = ''
                imgname = ''
                if len(var.errors) > 0 or len(var.failures):
                    imgname = '%s.png' % datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
                    imgpath = (sys.path[0] + self.s + 'output' + self.s + imgname)
                    self.browsedrive.get_screenshot_as_file(imgpath)
            except Exception as e:
                var = CustTestRult()
                self.logstu.error(e)
                var.errors = list(var.errors)
                var.errors[0][0].test_id = module_name + '.' + class_name
                var.errors[0][1] = str(e)
            iTestCase = self.caserult.get_TestCase(var, case_num=dict_row_data["案例编号"], title=dict_row_data["案例名称"],details=dict_row_data["案例详情"])
            self.iTestSuite.append(iTestCase)
        self.browsedrive.quit()

    def run_test(self, testdate={}):
        try:
            iTestCase = {}
            # 获取菜单对应的脚本名字和类名
            module_name = testdate['ModuleName']  # 需要导入的模块名
            class_name = testdate['ClassName']  # 需要导入的类名
            # 相同用例编号 case_num的用例，前面的失败了，后面的skip跳过测试，避免一个失败引起一堆失败
            if len(self.iTestSuite) > 1:
                last = len(self.iTestSuite) - 1
                if self.iTestSuite[last]['errors'] > 0 or self.iTestSuite[last]['failures'] > 0 or \
                                self.iTestSuite[last]['skipped'] > 0:
                    previous_step = ''
                    if self.iTestSuite[last]['errors'] > 0 or self.iTestSuite[last]['failures']:
                        previous_step = '上一步测试用例执行失败，当前步骤有依赖关系跳过执行 skipped.'
                    else:
                        previous_step = '上一步测试用例执行 skipped，当前步骤有依赖关系跳过执行 skipped.'
                    if self.iTestSuite[last]['case_num'] == testdate['case_num']:
                        iTestCase['case_num'] = testdate['case_num']  # 用例编号
                        iTestCase['environment'] = self.testENV
                        iTestCase['subsystem'] = self.testSys
                        iTestCase['title'] = testdate["case_title"]  # 案例名称
                        iTestCase['details'] = testdate["case_details"]  # 案例详情
                        iTestCase['run'] = 1
                        iTestCase['successes'] = 0
                        iTestCase['successes_str'] = ''
                        iTestCase['errors'] = 0
                        iTestCase['errors_str'] = ''
                        iTestCase['failures'] = 0
                        iTestCase['failures_str'] = ''
                        iTestCase['skipped'] = 1
                        iTestCase['skipped_str'] = [(module_name + '.' + class_name, previous_step)]
                        iTestCase['img'] = ''
                        iTestCase['start_time'] = self.iTestSuite[last]['stop_time']
                        iTestCase['stop_time'] = time.time()
                        iTestCase['time_consuming'] = iTestCase['stop_time'] - iTestCase['start_time']
                        self.iTestSuite.append(iTestCase)
                        return
            try:
                # 动态导入要执行的脚本类
                module = __import__(module_name)
                # 动态导入要执行的脚本对应的类
                exec_class = getattr(module, class_name)
                exec_class.Screenshotfilepath = self.Screenshotfilepath
                testunit = unittest.TestSuite()
                # 将测试用例加入到测试容器(套件)中
                testunit.addTest(unittest.makeSuite(exec_class))
                # 执行测试套件,失败重测，最多重复3次，最后一次或者成功的那一次写入测试结果中
                for j in range(0, 3):
                    testRunner = xmlrunner.XMLTestRunner(output=sys.path[0] + self.s + 'output',
                                                         outsuffix=testdate['test_order'])
                    testRunner.failfast = False
                    testRunner.buffer = False
                    testRunner.catchbreak = False
                    var = testRunner.run(testunit)
                    if len(var.errors) == 0 and len(var.failures) == 0:
                        self.logstu.info('Main Message:\n案例 %s|%s|%s 测试通过' % (testdate['case_num'], testdate["case_title"], testdate["case_details"]))
                        break
                    else:
                        self.logstu.info('Main Message:\n案例 %s|%s|%s 测试未通过' % (testdate['case_num'], testdate["case_title"], testdate["case_details"]))
                        continue
                    for fail in var.failures:
                        self.logstu.error('fail function: %s' % fail[0].test_id)
                        self.logstu.error('fail message: %s' % fail[1])
                    for error in var.errors:
                        self.logstu.error('error function: %s' % error[0].test_id)
                        self.logstu.error('error message: %s' % error[1])
            except Exception as e:
                var = CustTestRult()
                self.logstu.error(e)
                var.errors = list(var.errors)
                var.errors[0][0].test_id = module_name + '.' + class_name
                var.errors[0][1] = str(e)

            '''
            # 失败自动截图
            imgpath = ''
            imgname = ''
            if len(var.errors) > 0 or len(var.failures):
                imgname = '%s.png' % datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
                imgpath = (sys.path[0] + self.s + 'output' + self.s + imgname)
                if hasattr(exec_class,'browsedrive'):
                    self.browsedrive.get_screenshot_as_file(imgpath)
            '''
            # 更新测试结果集，生成各种版本的测试报告
        #     iTestCase['case_num'] = testdate['case_num']  # 用例编号
        #     iTestCase['environment'] = self.testENV
        #     iTestCase['subsystem'] = self.testSys
        #     iTestCase['title'] = testdate["case_title"]  # 案例名称
        #     iTestCase['details'] = testdate["case_details"]  # 案例详情
        #     iTestCase['run'] = len(var.successes) + len(var.errors) + len(var.failures) + len(var.skipped)
        #     iTestCase['successes'] = len(var.successes)
        #     iTestCase['successes_str'] = var.successes
        #     iTestCase['errors'] = len(var.errors)
        #     iTestCase['errors_str'] = var.errors
        #     iTestCase['failures'] = len(var.failures)
        #     iTestCase['failures_str'] = var.failures
        #     iTestCase['skipped'] = len(var.skipped)
        #     iTestCase['skipped_str'] = var.skipped
        #     iTestCase['img'] = ''  # imgname  # imgpath
        #     iTestCase['start_time'] = var.start_time
        #     iTestCase['stop_time'] = var.stop_time
        #     iTestCase['time_consuming'] = var.stop_time - var.start_time
        #     self.iTestSuite.append(iTestCase)
        # except Exception as e:
        #     self.logstu.error(e)
            # 更新测试结果集，生成各种版本的测试报告
            # self.caserult = UnitTestRultAct()
            iTestCase = self.caserult.get_TestCase(var, case_num=testdate['case_num'], title=testdate["case_title"],details=testdate["case_details"])
            self.iTestSuite.append(iTestCase)

        except Exception as e:
            self.logstu.error(e)


    def runScriptcase(self):
        self.logstu.info(u'运行从脚本中读取的用例')
        if self.IsGetDataFromDB == 'Y':
            TestCaseList = self.actdb.testCaseSel(self.actdb.scriptcaseSelSql)  # 获取测试用例列表
        elif self.IsGetDataFromDB == 'N':
            TestCaseList = self.sTC.get_scriptTestCaseList()

        # 循环执行测试，直到所有案例执行完毕
        for i in range(0,len(TestCaseList)):
            # 运行标志不是 1 的用例不运行测试
            if TestCaseList[i]['is_run'] != 1:
                self.logstu.debug('运行标识不为 1 的案例跳过：%s -- %s -- %s' % (TestCaseList[i]['test_order'], TestCaseList[i]['case_title'], TestCaseList[i]['case_details']))
                continue
            # 判断测试环境运行测试，排除非指定环境
            # if self.Env_Sys_Check(self.actdb.table[i]) == False:
            # continue
            # 流程控制
            '''
            if self.actdb.table[i]['act_type'] == 'Controller':
                if self.actdb.table[i]['run_mode'].upper() == 'IF':
                    self.IF_Controller(self.actdb.table[i], i)
                    continue
                if self.actdb.table[i]['run_mode'].upper() == 'FOR':
                    self.FOR_Controller(self.actdb.table[i], i)
                    continue
                self.logstu.error('流程控制符号 %s，在框架中没有这个逻辑。' % (self.actdb.table[i]['run_mode']))
            '''
            # 执行测试
            self.run_test(TestCaseList[i])

    def CreateReport(self):
        whtml = CreateHtmlReport()  # 生成测试报告
        whtml.removeFileInFirstDir(sys.path[0] + self.s + 'output')
        whtml.reportfile = sys.path[0] + self.s + 'output' + self.s + 'Report.html'
        whtml.templatefile = sys.path[0] + self.s + 'Utils' + self.s + 'ReportTemplate.html'
        whtml.iTestSuite = self.iTestSuite
        whtml.create_html_report()
        consoleReport = whtml.print_report()
        self.logstu.info(consoleReport)
        whtml.write_txt(sys.path[0] + self.s + 'output' + self.s + 'Report.txt', consoleReport)


if __name__ == '__main__':
    uitest = main_class()
    runModeList = uitest.runmode.split('|')
    for i in range(0,len(runModeList)):
        if runModeList[i] == 'runDBcase':
            try:
                uitest.runDBcase()
            except Exception as e:
                uitest.logstu.debug(e)
        elif runModeList[i] == 'runScriptcase':
            try:
                uitest.runScriptcase()
            except Exception as e:
                uitest.logstu.debug(e)
        else:
            print u'该模式未开发，请确认模式字段是否有误'

    # uitest.CreateReport()  # 生成报告
    print uitest.iTestSuite
    uitest.caserult.CreateReport(uitest.iTestSuite)  # 生成报告

