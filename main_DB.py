#coding=utf-8
import unittest,sys,os,time, logging, xmlrunner, datetime,ConfigParser,MySQLdb
from selenium import webdriver
from Utils.writeReport import CreateHtmlReport
#这里需要导入测试文件
from Utils.commFunction import CommFunction
from Utils.logger import Logger
from Utils.testMySqlAct import TestMySqlAct
from Utils.lyFunction import PubFunction

reload(sys)
sys.setdefaultencoding('utf8')
s = os.sep
pubf = PubFunction()
comm = CommFunction()
# 读取配置文件
cf = ConfigParser.ConfigParser()
cf.read('test.conf')
db_host = cf.get('db', 'host')
db_port = cf.getint('db', 'port')
db_name = cf.get('db', 'db')
db_user = cf.get('db', 'user')
db_passwd = cf.get('db', 'passwd')
db_charset = cf.get('db', 'charset')
# print  db_charset #db_host  +','+db_name+','+db_user+','+db_passwd+','+db_port+','+db_charset
#连接数据库
actdb = TestMySqlAct(host=db_host, db=db_name, user=db_user, passwd=db_passwd, port=db_port,charset=db_charset)
#把测试用例表testcase的数据更新到执行表
actdb.table = actdb.testCaseSel(actdb.testcaseSelSql) # 获取测试用例列表
actdb.table_copy = actdb.testCaseSel(actdb.testcase_copySelSql) # 获取测试用例列表
str1 = ''
for k in range(0, len(actdb.table_copy)):
    if str1 == '':
        str1 = str(actdb.table_copy[k]['test_id'])
    else:
        str1 = str1 + ','+ str(actdb.table_copy[k]['test_id'])
chrild_cellstr = str1.split(",")
for i in range(0,len(actdb.table)):
    if str(actdb.table[i]['test_id']) in chrild_cellstr:
        for j in range(0,len(actdb.table_copy)):
            if actdb.table[i]['test_id'] == actdb.table_copy[j]['test_id']:
                actdb.UpdateCaseRecord(i)
                break
    else:
        print 'testcase: '+str(actdb.table[i]['test_id'])+' '+actdb.table[i]['case_details']
        actdb.insertRecord(i)

# actdb = TestMySqlAct(host = '10.18.12.198', db = 'autotest', user = 'root', passwd = '111111', port = 3306, charset='utf8')
actdb.testCaseDel('TRUNCATE webuiruntime') # 删除临时表数据

# copy 需要执行的测试用例到临时表
actdb.testCaseUpdate('INSERT INTO webuiruntime SELECT * FROM webuicase')
actdb.table = pubf.dict_None_to_Str(actdb.testCaseSel(actdb.caseselstr))

alltestnum = len(actdb.table) # 需要执行用例的个数
logstu = Logger(sys.path[0] + s + 'logs' + s + 'autotest.log',logging.INFO,logging.DEBUG) # ERROR
#获取菜单对应脚本矩阵
dict_menu_script = comm.get_menu_to_script()
#执行脚本对应的脚本类名
scriptname = ""
#启动浏览器,返回浏览器对象
browserName = 'Chrome'
# browsedrive = comm.get_browserdrvie('Firefox')
browsedrive = comm.get_browserdrvie(browserName)
print "start -  -   -"

# 测试环境设置
# sonSys = 'CBS'
sonSys = 'NCP'
testENV = 'UAT' # 环境默认值 uat， 还有stg等
if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        print "Start Parameter:", i, sys.argv[i]
        if sys.argv[i].find("=") != -1:
            tmp = sys.argv[i].split('=')
            if tmp[0].upper()=='S' or tmp[0].upper()=='SYS':
                sonSys = tmp[1]
            if tmp[0].upper()=='V' or tmp[0].upper()=='ENV':
                testENV = tmp[1]
        else:
            testENV = sys.argv[1]
            if i == 2:
                sonSys = sys.argv[2]

#循环读取测试数据
iTestSuite = []
whtml = CreateHtmlReport()
whtml.removeFileInFirstDir(sys.path[0] + s + 'output')
for i in range(0,alltestnum):
    # 运行标志不是 1 的用例不运行测试
    if actdb.table[i]['is_run'] != 1:
        logstu.debug('运行标识不为 1 的案例跳过：%s -- %s -- %s' % (actdb.table[i]['test_order'], actdb.table[i]['case_title'], actdb.table[i]['case_details']))
        continue
    # 判断测试环境运行测试，排除非指定环境
    if testENV.find(',') == -1:
        if actdb.table[i]['environment'].upper() != testENV.upper():
            continue
    else:
        vflag = False;
        for env in testENV.split(','):
            if actdb.table[i]['environment'].upper() == env.upper():
                vflag = True;
        if vflag == False:
            continue
    # 判断子系统
    if sonSys.find(',') == -1:
        if actdb.table[i]['subsystem'].upper() != sonSys.upper():
            continue
    else:
        sflag = False;
        for son in sonSys.split(','):
            if actdb.table[i]['subsystem'].upper() == son.upper():
                sflag = True;
        if sflag == False:
            continue;
    try:
        iTestCase = {}
        # 将数据库查询得到的字典的key替换为中文
        dict_row_data = pubf.dict_key_update(actdb.table[i], actdb.casetitle_cn)
        # 对数据中的特殊字段做处理，如rd(10) up(1)等
        dict_row_data = actdb.rowdata_update(dict_row_data, i)
        # 获取最后一级的菜单名
        menuname = ''
        if dict_row_data['一级菜单'] != None and dict_row_data['一级菜单'] != '':
            menuname = pubf.all_type_to_encode(dict_row_data['一级菜单']).strip()
        if dict_row_data['二级菜单'] != None and dict_row_data['二级菜单'] != '':
            menuname = pubf.all_type_to_encode(dict_row_data['二级菜单']).strip()
        if dict_row_data['三级菜单'] != None and dict_row_data['三级菜单'] != '':
            menuname = pubf.all_type_to_encode(dict_row_data['三级菜单']).strip()
        logstu.debug('当前操作：%s' % menuname)
        # 获取菜单对应的脚本名字和类名 ？？？？？？？？？
        actObject = pubf.all_type_to_encode(dict_row_data['操作对象']).strip()
        print actObject
        dict_menu_script[actObject]
        LoadScriptObject = dict_menu_script[actObject].split("|")
        module_name = LoadScriptObject[0]  # 需要导入的模块名
        class_name = LoadScriptObject[1]  # 需要导入的类名
        # menutemp = dict_menu_script[menuname].split("|")
        # module_name = menutemp[0] # 需要导入的模块名
        # class_name = menutemp[1] # 需要导入的类名
        logstu.debug('导入类：%s, class：%s' % (module_name, class_name))
        # 相同用例编号 case_num的用例，前面的失败了，后面的skip跳过测试，避免一个失败引起一堆失败
        if len(iTestSuite) > 1:
            last = len(iTestSuite) - 1
            if iTestSuite[last]['errors'] > 0 or iTestSuite[last]['failures'] > 0 or iTestSuite[last]['skipped'] > 0:
                previous_step = ''
                if iTestSuite[last]['errors'] > 0 or iTestSuite[last]['failures']:
                    previous_step = '上一步测试用例执行失败，当前步骤有依赖关系跳过执行 skipped.'
                else:
                    previous_step = '上一步测试用例执行 skipped，当前步骤有依赖关系跳过执行 skipped.'
                if iTestSuite[last]['case_num'] == dict_row_data['案例编号']:
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
                    iTestCase['start_time'] = iTestSuite[last]['stop_time']
                    iTestCase['stop_time'] = time.time()
                    iTestCase['time_consuming'] = iTestCase['stop_time'] - iTestCase['start_time']
                    iTestSuite.append(iTestCase)
                    continue

        if (dict_row_data["登录用户"] <> "" and dict_row_data["登录密码"] <> "") and dict_row_data["子系统"] <> "ncp":
            browsedrive.quit()
            browsedrive = comm.login_success(dict_row_data["子系统"],dict_row_data["登录地址"], dict_row_data["登录用户"], dict_row_data["登录密码"],browserName)
        else:
            browsedrive.quit()

        #动态导入要执行的脚本类
        module = __import__(module_name)
        #动态导入要执行的脚本对应的类
        exec_class = getattr(module,class_name)
        #把测试数据传送给执行脚本里的类
        exec_class.mainWebDr = browsedrive
        exec_class.comm = comm
        exec_class.dict_data = dict_row_data
        exec_class.logstu = logstu
        exec_class.actdb = actdb
        exec_class.row = i
        testunit=unittest.TestSuite()
        #将测试用例加入到测试容器(套件)中
        testunit.addTest(unittest.makeSuite(exec_class))
        # 执行测试套件,失败重测，最多重复3次，最后一次或者成功的那一次写入测试结果中
        for j in range(0, 2):
            testRunner = xmlrunner.XMLTestRunner(output=sys.path[0] + s + 'output')  # ,outsuffix='wow2'
            testRunner.failfast = False
            testRunner.buffer = False
            testRunner.catchbreak = False
            var = testRunner.run(testunit)
            if len(var.errors) == 0:
                break
            logstu.debug('error case num: %d\nfail case num: %d\ntime consuming: %s' % (
            len(var.errors), len(var.failures), var.stop_time - var.start_time))
            for fail in var.failures:
                logstu.error('fail function: %s' % fail[0].test_id)
                logstu.error('fail message: %s' % fail[1])
            for error in var.errors:
                logstu.error('error function: %s' % error[0].test_id)
                logstu.error('error message: %s' % error[1])

        imgpath = ''
        imgname = ''
        if len(var.errors)>0 or  len(var.failures):
            imgname = '%s.png' % datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
            imgpath = (sys.path[0] + s + 'output' + s + imgname)
            browsedrive.get_screenshot_as_file(imgpath)
        iTestCase['case_num'] = dict_row_data["案例编号"]
        iTestCase['environment'] = dict_row_data['环境']
        iTestCase['subsystem'] = dict_row_data['子系统']
        iTestCase['title'] = dict_row_data["案例名称"]
        iTestCase['details'] = dict_row_data["案例详情"]
        iTestCase['run'] = len(var.successes) + len(var.errors) + len(var.failures) + len(var.skipped)
        iTestCase['successes'] = len(var.successes)
        iTestCase['successes_str'] = var.successes
        iTestCase['errors'] = len(var.errors)
        iTestCase['errors_str'] = var.errors
        iTestCase['failures'] = len(var.failures)
        iTestCase['failures_str'] = var.failures
        iTestCase['skipped'] = len(var.skipped)
        iTestCase['skipped_str'] = var.skipped
        iTestCase['img'] = imgname #imgpath
        iTestCase['start_time'] = var.start_time
        iTestCase['stop_time'] = var.stop_time
        iTestCase['time_consuming'] = var.stop_time - var.start_time
        iTestSuite.append(iTestCase)
    except Exception as e:
        logstu.error(e)
        continue
browsedrive.quit()

whtml.reportfile = sys.path[0] + s + 'output' + s + 'Report.html'
whtml.templatefile = sys.path[0] + s + 'Utils'+ s +'ReportTemplate.html'
whtml.iTestSuite = iTestSuite
whtml.create_html_report()
alltest_count = len(iTestSuite)
consoleReport = whtml.print_report()
logstu.info(consoleReport)
whtml.write_txt(sys.path[0] + s + 'output'+ s +'Report.txt', consoleReport)