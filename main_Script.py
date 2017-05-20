#coding=utf-8
import unittest,sys,time, logging, xmlrunner, datetime
from Utils.writeReport import CreateHtmlReport
from Utils.logger import Logger
from Utils.CustTestRult import CustTestRult
from Utils.UnitTestRultAct import UnitTestRultAct
import sys, os
reload(sys)
sys.setdefaultencoding('utf8')

class Main_UITest(object):
    s = os.sep
    logstu = Logger(sys.path[0] + s + 'logs' + s + 'autotest.log', logging.INFO, logging.DEBUG)  # ERROR
    testSys = 'ALL'  # CBS carloan
    testENV = 'ALL'  # 环境默认值 UAT1， 还有stg等
    TestCaseList = [] # 测试模块及标题列表
    iTestSuite = [] # 测试结果集
    retestnum = 3 # 失败重测次数，按测试模块计算，默认为 3

    def run_test(self, testdate={}):
        try:
            iTestCase = {}
            # 获取菜单对应的脚本名字和类名
            module_name = testdate['ModuleName']  # 需要导入的模块名
            class_name = testdate['ClassName']  # 需要导入的类名
            # 相同用例编号 case_num的用例，前面的失败了，后面的skip跳过测试，避免一个失败引起一堆失败
            if len(self.iTestSuite) > 0:
                last = len(self.iTestSuite) - 1
                if self.iTestSuite[last]['errors'] > 0 or self.iTestSuite[last]['failures'] > 0 or self.iTestSuite[last]['skipped'] > 0:
                    previous_step = ''
                    if self.iTestSuite[last]['errors'] > 0 or self.iTestSuite[last]['failures']> 0:
                        previous_step = '上一步测试用例执行失败，当前步骤有依赖关系跳过执行 skipped.'
                    else:
                        previous_step = '上一步测试用例执行 skipped，当前步骤有依赖关系跳过执行 skipped.'
                    if self.iTestSuite[last]['case_num'] == testdate['caseNum']:
                        iTestCase['case_num'] = testdate['caseNum']  # 用例编号
                        iTestCase['environment'] = testdate['ENV'] if testdate.has_key('ENV') else '-' #self.testENV
                        iTestCase['subsystem'] = testdate['SYS'] if testdate.has_key('SYS') else '-' #self.testENVself.testSys
                        iTestCase['title'] = testdate["title"]      # 案例名称
                        iTestCase['details'] = testdate["details"]  # 案例详情
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
                testunit = unittest.TestSuite()
                # 将测试用例加入到测试容器(套件)中
                testunit.addTest(unittest.makeSuite(exec_class))
                # 执行测试套件,失败重测，最多重复3次，最后一次或者成功的那一次写入测试结果中
                if isinstance(self.retestnum, int):
                    if self.retestnum < 1 or self.retestnum > 10:
                        self.retestnum = 3
                else:
                    self.retestnum = 3
                for j in range(0, self.retestnum):
                    testRunner = xmlrunner.XMLTestRunner(output=sys.path[0] + self.s + 'output',outsuffix=testdate['test_order'])
                    testRunner.failfast = False
                    testRunner.buffer = False
                    testRunner.catchbreak = False
                    var = testRunner.run(testunit)
                    if len(var.errors) == 0 and len(var.failures) == 0:
                        self.logstu.info('Main Message:\n案例 %s|%s|%s 测试通过' % (
                        testdate['caseNum'], testdate["title"], testdate["details"]))
                        break
                    else:
                        self.logstu.info('Main Message:\n案例 %s|%s|%s 测试未通过' % (
                        testdate['caseNum'], testdate["title"], testdate["details"]))
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
            # 更新测试结果集，生成各种版本的测试报告
            caserult = UnitTestRultAct()
            iTestCase = caserult.get_TestCase(var,case_num=testdate['caseNum'], title=testdate["title"],details=testdate["details"])
            self.iTestSuite.append(iTestCase)
        except Exception as e:
            self.logstu.error(e)

    def TestStar(self):
        # 循环执行测试，直到所有案例执行完毕
        for testdate in self.TestCaseList:
            # 判断测试环境运行测试，排除非指定环境
            #if self.Env_Sys_Check(self.actdb.table[i]) == False:
                #continue
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
            self.run_test(testdate)
        caserult = UnitTestRultAct()
        caserult.CreateReport(self.iTestSuite) # 生成报告
        #self.CreateReport() # 生成报告

################################ 以下是测试逻辑中使用的方法 #################################
    # 判断执行环境
    def Env_Sys_Check(self, testdate={}):
        # 判断测试环境运行测试，排除非指定环境
        if self.testENV.upper() != 'ALL':
            if self.testENV.find(',') == -1:
                if testdate['sys_env'].upper() != self.testENV.upper():
                    return False
            else:
                vflag = False;
                for env in self.testENV.split(','):
                    if testdate['sys_env'].upper() == env.upper():
                        vflag = True;
                if vflag == False:
                    return False
        # 判断系统
        if self.testSys.upper() != 'ALL':
            if self.testSys.find(',') == -1:
                if testdate['chrild_sys'].upper() != self.testSys.upper():
                    return False
            else:
                sflag = False;
                for son in self.testSys.split(','):
                    if testdate['chrild_sys'].upper() == son.upper():
                        sflag = True;
                if sflag == False:
                    return False;
        return True
    # if 流程控制
    def IF_Controller(self, testdate={}):
        pass
    # for流程控制
    def FOR_Controller(self, testdate={}):
        pass
    def CreateReport(self):
        whtml = CreateHtmlReport()  # 生成测试报告
        whtml.removeFileInFirstDir(sys.path[0] + self.s + 'output')
        # 设置html测试报告输出位置
        whtml.reportfile = sys.path[0] + self.s + 'output' + self.s + 'Report.html'
        # 设置html测试报告模板文件位置
        whtml.templatefile = sys.path[0] + self.s + 'Utils' + self.s + 'ReportTemplate.html'
        # 设置报告的内容集合
        whtml.iTestSuite = self.iTestSuite
        # 生成html报告
        whtml.create_html_report()
        # 屏幕打印测试报告
        consoleReport = whtml.print_report()
        self.logstu.info(consoleReport)
        # 生成文本格式简易测试报告
        whtml.write_txt(sys.path[0] + self.s + 'output' + self.s + 'Report.txt', consoleReport)


if __name__ == '__main__':
    # test_order：测试案例唯一标识，失败重测需要根据这个指示覆盖测试xml报告，以避免jenkins重复计数
    # caseNum：测试案例编号，依赖用例编号需要相同，用以实现依赖用例上游执行失败，下游的用例跳过不执行，避免大片失败
    # ModuleName：测试模块文件路径package
    # ClassName：测试模块中的测试类名称
    TestCaseList = [
        {'caseNum':'test001','test_order':'0001','ModuleName':'Sys_NCP.TestClass.TestLogin', 'ClassName':'TestLogin', 'title':'标题1', 'details':'详细测试内容1'},
        {'caseNum':'test002','test_order':'0002','ModuleName':'Sys_NCP.TestClass.Test2', 'ClassName':'Test2', 'title':'标题2', 'details':'详细测试内容2'},
        {'caseNum': 'test003', 'test_order': '0003', 'ModuleName': 'Sys_NCP.TestClass.ContractQuery','ClassName': 'ContractQuery', 'title': '合同管理', 'details': '合同查询'},
        {'caseNum': 'test004', 'test_order': '0004', 'ModuleName': 'Sys_NCP.TestClass.SysManage','ClassName': 'SysManage', 'title': '系统管理', 'details': '角色管理'},
        {'caseNum': 'test005', 'test_order': '0005', 'ModuleName': 'Sys_NCP.TestClass.CountManage','ClassName': 'CountManage', 'title': '账户管理', 'details': '账户综合信息查询'}
    ]
    TestCaseList = [
        {'caseNum': 'test001', 'test_order': '0001', 'ModuleName': 'Sys_Carloan.TestClass.TestAdmin',
         'ClassName': 'TestAdmin', 'title': 'CarLoan Page Check', 'details': 'Admin All Page Check'},
        # {'caseNum': 'ContractQuery001', 'test_order': '1001','ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3144_NCP5',
        #  'ClassName': 'checkMainPageElement', 'title': '合同管理', 'details': '验证主界面的界面元素'},
        # {'caseNum': 'ContractQuery002', 'test_order': '1002','ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3145_NCP5',
        #  'ClassName': 'checkContractQueryPageElement', 'title': '合同查询', 'details': '合同查询_页面元素识别'},
        # {'caseNum': 'ContractQuery003', 'test_order': '1003','ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3146_NCP6',
        #  'ClassName': 'ContractQuery_SingleCondition', 'title': '合同查询', 'details': '查询功能-单个条件查询功能'},
        # {'caseNum': 'ContractQuery004', 'test_order': '1004','ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3147_NCP6',
        #  'ClassName': 'ContractQuery_CombinationCondition', 'title': '合同查询', 'details': '合同查询_组合条件查询'},
        # {'caseNum': 'ContractQuery005', 'test_order': '1005','ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3148_NCP8',
        #  'ClassName': 'ContractQuery_FormOperation', 'title': '合同查询', 'details': '合同查询_对表单数据操作'},
        # {'caseNum': 'test2001', 'test_order': '2001','ModuleName': 'Sys_NCP.TestClass.TestLogin','ClassName': 'TestLogin', 'title': '登录', 'details': '登录成功'},
        # {'caseNum': 'test2003', 'test_order': '2003','ModuleName': 'Sys_NCP.TestClass.ContractQuery',
        #  'ClassName': 'ContractQuery', 'title': '合同管理', 'details': '合同查询'},
        # {'caseNum': 'test2004', 'test_order': '2004', 'ModuleName': 'Sys_NCP.TestClass.SysManage',
        #  'ClassName': 'SysManage', 'title': '系统管理', 'details': '角色管理'},
        # {'caseNum': 'test2005', 'test_order': '2005', 'ModuleName': 'Sys_NCP.TestClass.checkMainPage',
        #  'ClassName': 'CheckMainPage', 'title': 'NCP_验证主界面', 'details': 'NCP_验证主界面的界面元素'},
        #{'caseNum': 'test2006', 'test_order': '2006', 'ModuleName': 'Sys_CBS.TestClass.CBScheckMainPage',
         #'ClassName': 'CheckMainPage', 'title': 'CBS_验证主界面', 'details': 'CBS_验证主界面的界面元素'},
    ]

    uitest = Main_UITest()
    uitest.TestCaseList = TestCaseList
    uitest.TestStar()