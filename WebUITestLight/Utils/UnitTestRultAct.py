# -*- coding: UTF-8 -*-
import time, os, sys, re
from WebUITestLight.Utils.writeReport import CreateHtmlReport

class UnitTestRultAct(object):
    var = None # unittest 运行后生成的测试结果
    # iTestSuite: [{'errors': 0, 'run': 5, 'title': 'title test case', 'successes': 3, 'start_time': 1465701759.936, 'skipped_str': [(<xmlrunner.result._TestInfo object at 0x00000000027EE4E0>, 'demonstrating skipping')], 'failures_str': [(<xmlrunner.result._TestInfo object at 0x00000000027EE278>, 'Traceback (most recent call last):\n  File "D:\\PythonWorks\\MyPyTestOne\\stu_unitest\\junitreport.py", line 35, in test_failed\n    self.assertEqual(1,2)\nAssertionError: 1 != 2\n')], 'errors_str': [], 'skipped': 1, 'details': 'test case details', 'failures': 1, 'time_consuming': 0.0, 'stop_time': 1465701759.936},
    #              {'errors': 0, 'run': 3, 'title': 'title test case', 'successes': 3, 'start_time': 1465701759.947, 'skipped_str': [], 'failures_str': [], 'errors_str': [], 'skipped': 0, 'details': 'test case details', 'failures': 0, 'time_consuming': 2.0, 'stop_time': 1465701761.947}
    #             ]

    def get_TestCase(self, var,case_num='', title='测试类标题', details='测试内容详情', img=''):
        iTestCase = {}
        # 更新测试结果集，生成各种版本的测试报告
        if case_num == '':
            iTestCase['case_num'] = str(var._previousTestClass)  # 测试类class对象
        else:
            iTestCase['case_num'] = case_num  # 测试类class对象
        iTestCase['environment'] = '-'
        iTestCase['subsystem'] = '-'
        iTestCase['title'] = title
        iTestCase['details'] = details
        iTestCase['run'] = len(var.successes) + len(var.errors) + len(var.failures) + len(var.skipped)
        iTestCase['successes'] = len(var.successes)
        iTestCase['successes_str'] = var.successes
        iTestCase['errors'] = len(var.errors)
        iTestCase['errors_str'] = var.errors
        iTestCase['failures'] = len(var.failures)
        iTestCase['failures_str'] = var.failures
        iTestCase['skipped'] = len(var.skipped)
        iTestCase['skipped_str'] = var.skipped
        iTestCase['img'] = img  # 图片地址 imgname  # imgpath
        iTestCase['start_time'] = var.start_time
        iTestCase['stop_time'] = var.stop_time
        iTestCase['time_consuming'] = var.stop_time - var.start_time
        return iTestCase

    def CreateReport(self,iTestSuite,strcode = 'utf-8'):#, propath='WebUITestLight'
        whtml = CreateHtmlReport()  # 生成测试报告
        # 设置html测试报告输出位置
        whtml.reportfile = sys.path[0] + '/output/HtmlReport.html'
        # 设置html测试报告模板文件位置
        #programpath = sys.path[0][:sys.path[0].find(propath)]
        #print programpath
        #whtml.templatefile = programpath +propath+'/Utils/ReportTemplate.html'
        whtml.templatefile = os.path.dirname(os.path.realpath(__file__))+'/ReportTemplate.html'
        # 设置报告的内容集合
        whtml.iTestSuite = iTestSuite
        # 生成html报告
        whtml.create_html_report()
        # 屏幕打印测试报告
        consoleReport = whtml.print_report()
        print (consoleReport.encode(strcode))
        # 生成文本格式简易测试报告
        whtml.write_txt(sys.path[0] + '/output/TxtReport.txt', consoleReport)

if __name__ == '__main__':
    pass