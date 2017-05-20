# -*- coding: UTF-8 -*-
import time, os, sys, re
class CreateHtmlReport(object):
    templatefile = 'ReportTemplate.html'
    reportfile = 'Report.html'
    iTestSuite = []
    # iTestSuite: [{'errors': 0, 'run': 5, 'title': 'title test case', 'successes': 3, 'start_time': 1465701759.936, 'skipped_str': [(<xmlrunner.result._TestInfo object at 0x00000000027EE4E0>, 'demonstrating skipping')], 'failures_str': [(<xmlrunner.result._TestInfo object at 0x00000000027EE278>, 'Traceback (most recent call last):\n  File "D:\\PythonWorks\\MyPyTestOne\\stu_unitest\\junitreport.py", line 35, in test_failed\n    self.assertEqual(1,2)\nAssertionError: 1 != 2\n')], 'errors_str': [], 'skipped': 1, 'details': 'test case details', 'failures': 1, 'time_consuming': 0.0, 'stop_time': 1465701759.936},
    #              {'errors': 0, 'run': 3, 'title': 'title test case', 'successes': 3, 'start_time': 1465701759.947, 'skipped_str': [], 'failures_str': [], 'errors_str': [], 'skipped': 0, 'details': 'test case details', 'failures': 0, 'time_consuming': 2.0, 'stop_time': 1465701761.947}
    #             ]

    starttime = 0
    endtime = 0
    testpass = 0
    testfail = 0
    testerror = 0
    testskipped = 0

    html_test_trtop = '''
    <tr id='$id' class='$class'>
        <td>$title</td>
        <td name="environment" nowrap>$environment</td>
        <td name="subsystem">$subsystem</td>
        <td name="num_count">$num_count</td>
        <td name="num_pass">$num_pass</td>
        <td name="num_fail">$num_fail</td>
        <td name="num_error">$num_error</td>
        <td name="num_skip">$num_skipped</td>
        <td class="showerrimg" onclick="showClassDetail2(this)" nowrap>Detail</td>
    </tr>
    '''
    # $detail_id = ptonetest.1  ftonetest.1  表示html_test_trtop中tr id值加上前缀pt表成功，ft表失败，后缀'.1' 有多个测试方法就依次增加数字
    # $caseclass = testcase passCase failCase errorCase
    html_test_trdetail = '''
    <tr id='$detail_id' class='hiddenRow'>
        <td class='none'><div class='$caseclass'>$testcase</div></td>
        <td colspan='8' align='center'>
            <a onfocus='this.blur();' onclick="shownextSiblingDiv(this)" >$state</a>
            <div class="popup_window">
                <div style='text-align: right; color:red;cursor:pointer'>
                    <a onfocus='this.blur();' onclick="this.parentNode.parentNode.style.display = 'none' " >[x]</a>
                </div>
                <pre>
                    $pre
                </pre>
                $img
            </div>
            <!--css div popup end-->
        </td>
    </tr>
    '''
    Classification_Statistics = '''
        <tr bgcolor="LightSteelBlue">
        <td nowrap>$env</td>
    	 <td nowrap>$system</td>
        <td nowrap>$num_pass</td>
        <td nowrap><font color="red">$num_fail</font></td>
        <td nowrap><font color="red">$num_error</font></td>
        <td nowrap><font color="SlateGray">$num_skipped</font></td>
        </tr>
        '''

    def read_html_template(self):
        # 读取模板
        fo = open(self.templatefile, "r+")
        str = fo.read();
        # 关闭打开的模板文件
        fo.close()
        return str

    def create_html_report(self):
        # 写入html报告
        fo = open(self.reportfile, "wb")
        htmldata = self.testdata_to_html()
        htmlCS = self.Classification_Statistics_to_html()
        html = self.read_html_template()
        html = html.replace('$tr_data',htmldata)
        html = html.replace('$Classification_Statistics', htmlCS)

        html = html.replace('$StartTime', str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.starttime))))
        html = html.replace('$EndTime', str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.endtime))))
        durtime = int(self.endtime - self.starttime)
        if durtime > 3600:
            durtimestr = str(durtime/3060) + ' h ' + str((durtime%3600)/60) + ' min ' + str((durtime%3600)%60) + ' sec'
        elif durtime > 60:
            durtimestr = str(durtime/60) + ' min ' + str(durtime%60) + ' sec'
        else:
            durtimestr = '%.2f' % (self.endtime - self.starttime) + ' sec'#durtimestr = str(durtime) + ' s'
        html = html.replace('$Duration', durtimestr)
        html = html.replace('$Status','Pass ' + str(self.testpass) + ' Failure ' + str(self.testfail)
                            + ' Error ' + str(self.testerror) + ' Skipped ' + str(self.testskipped))
        fo.write(html);
        # 关闭打开的html报告文件
        fo.close()

    # 生成html报告中统计各系统各环境的统计信息
    def Classification_Statistics_to_html(self):
        lentestCase = len(self.iTestSuite)
        if lentestCase == 0:
            return '无测试数据！'
        env_sys_list = self.Env_Sys_TongJi()
        tr_tongji = ''
        for env_sys in env_sys_list:
            tr_for = self.Classification_Statistics
            tr_for = tr_for.replace('$env', env_sys['environment'])
            tr_for = tr_for.replace('$system', env_sys['subsystem'])
            tr_for = tr_for.replace('$num_pass', str(env_sys['successes']))
            tr_for = tr_for.replace('$num_fail', str(env_sys['failures']))
            tr_for = tr_for.replace('$num_error', str(env_sys['errors']))
            tr_for = tr_for.replace('$num_skipped', str(env_sys['skipped']))
            tr_tongji = tr_tongji + tr_for
        return tr_tongji

    def testdata_to_html(self):
        lentestCase = len(self.iTestSuite)
        if lentestCase == 0:
            return '无测试数据！'

        trall = ''
        for i in range(0, lentestCase):
            if self.starttime == 0 or self.starttime > self.iTestSuite[i]['start_time']:
                self.starttime = self.iTestSuite[i]['start_time']
            if self.endtime == 0 or self.endtime < self.iTestSuite[i]['stop_time']:
                self.endtime = self.iTestSuite[i]['stop_time']
            self.testpass = self.testpass + self.iTestSuite[i]['successes']
            self.testfail = self.testfail + self.iTestSuite[i]['failures']
            self.testerror = self.testerror + self.iTestSuite[i]['errors']
            self.testskipped = self.testskipped + self.iTestSuite[i]['skipped']
            trtop = self.html_test_trtop
            trtop_id = 'Test' + str(i)
            trtop = trtop.replace('$id', trtop_id) # 定义测试类id
            # 定义测试类class
            if self.iTestSuite[i]['run'] == self.iTestSuite[i]['successes']:
                trtop = trtop.replace('$class', 'passClass')
            else:
                if self.iTestSuite[i]['errors'] > 0:
                    trtop = trtop.replace('$class', 'errorClass')
                elif self.iTestSuite[i]['failures'] > 0:
                    trtop = trtop.replace('$class', 'failClass')
                elif self.iTestSuite[i]['skipped'] > 0:
                    trtop = trtop.replace('$class', 'skipClass')
            trtop = trtop.replace('$title', self.iTestSuite[i]['title'] + '<br>' + self.iTestSuite[i]['details'])
            trtop = trtop.replace('$environment', str(self.iTestSuite[i]['environment']))
            trtop = trtop.replace('$subsystem', str(self.iTestSuite[i]['subsystem']))
            trtop = trtop.replace('$num_count', str(self.iTestSuite[i]['run']))
            trtop = trtop.replace('$num_pass', str(self.iTestSuite[i]['successes']))
            trtop = trtop.replace('$num_fail', str(self.iTestSuite[i]['failures']))
            trtop = trtop.replace('$num_error', str(self.iTestSuite[i]['errors']))
            trtop = trtop.replace('$num_skipped', str(self.iTestSuite[i]['skipped']))
            trdetail = ''
            idnum = 0
            if self.iTestSuite[i]['failures'] > 0:
                for fail in self.iTestSuite[i]['failures_str']:
                    trdetail = trdetail + '\n' + self.html_test_trdetail
                    trdetail = trdetail.replace('$pre', fail[1]) # track message
                    trdetail = trdetail.replace('$caseclass', 'failCase')
                    trdetail = trdetail.replace('$testcase', str(fail[0].test_id))
                    trdetail = trdetail.replace('$state', 'fail')
                    trdetail_id = 'ft' + trtop_id + '.' + str(idnum)
                    idnum = idnum + 1
                    trdetail = trdetail.replace('$detail_id', trdetail_id)
            if self.iTestSuite[i]['errors'] > 0:
                # $caseclass = testcase passCase failCase errorCase
                for error in self.iTestSuite[i]['errors_str']:
                    trdetail = trdetail + '\n' + self.html_test_trdetail
                    trdetail_id = 'ft' + trtop_id + '.' + str(idnum)
                    idnum = idnum + 1
                    trdetail = trdetail.replace('$detail_id', trdetail_id)
                    trdetail = trdetail.replace('$pre', error[1])  # track message
                    trdetail = trdetail.replace('$caseclass', 'errorCase')
                    trdetail = trdetail.replace('$testcase', error[0].test_id)
                    trdetail = trdetail.replace('$state', 'error')
            if self.iTestSuite[i]['skipped'] > 0:
                for skip in self.iTestSuite[i]['skipped_str']:
                    trdetail = trdetail + '\n' + self.html_test_trdetail
                    trdetail_id = 'ft' + trtop_id + '.' + str(idnum)
                    idnum = idnum + 1
                    trdetail = trdetail.replace('$detail_id', trdetail_id)
                    trdetail = trdetail.replace('$pre', skip[1])  # track message
                    trdetail = trdetail.replace('$caseclass', 'skipCase')
                    trdetail = trdetail.replace('$testcase', skip[0])
                    trdetail = trdetail.replace('$state', 'skipped')
            if self.iTestSuite[i]['successes'] > 0:
                for succ in self.iTestSuite[i]['successes_str']:
                    trdetail = trdetail + '\n' + self.html_test_trdetail
                    trdetail_id = 'pt' + trtop_id + '.' + str(idnum)
                    idnum = idnum + 1
                    trdetail = trdetail.replace('$detail_id', trdetail_id)
                    trdetail = trdetail.replace('$pre', succ.test_description)
                    trdetail = trdetail.replace('$caseclass', 'passCase')
                    trdetail = trdetail.replace('$testcase', succ.test_id)
                    trdetail = trdetail.replace('$state', 'pass')
            if self.iTestSuite[i]['img'] != '':
                trdetail = trdetail.replace('$img', '<img src="' + self.iTestSuite[i]['img'] + '" width="800" >')
            else:
                trdetail = trdetail.replace('$img', '')
            trdetail = self.codetocnstr(trdetail)
            trall = trall + '\n'+ self.all_type_to_encode(trtop) + self.all_type_to_encode(trdetail)
        return trall

    # 判断字符串是否有unicode，如果有解码为utf8格式
    def all_type_to_encode(self, value):
        if isinstance(value, unicode):
            return value.encode('utf8')
        else:
            return value

    def print_report(self):
        alltest_count = len(self.iTestSuite) # test class num
        alltestdef = 0
        ctime = int(self.endtime - self.starttime)
        ctime_str = str(ctime / 60) + ' min ' + str(ctime % 60) + ' sec'
        env_sys_list = self.Env_Sys_TongJi()
        env_sys_str = '  ENV  System  Pass  Failure  Error  Skipped\n'
        for env_sys in env_sys_list:
            env_sys_str = env_sys_str + '  %s  %s  %d  %d  %d  %d\n' % (
            env_sys['environment'], env_sys['subsystem'], env_sys['successes'], env_sys['failures'], env_sys['errors'],
            env_sys['skipped'])

        report_str = '\n-------------------------------------------------------\n' \
                     + 'AutoTest Result\n' \
                     + 'Start Time:' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.starttime))) \
                     + '\nEnd Time:' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.endtime))) \
                     + '\nTime Consuming:' + ctime_str \
                     + '\nStatus:' + 'Pass ' + str(self.testpass) + ' Failure ' + str(self.testfail) + ' Error ' \
                     + str(self.testerror) + ' Skipped ' + str(self.testskipped) + '\n' \
                     + '=====================================================================\n' \
                     + env_sys_str \
                     + '=====================================================================\n' \
                     + '#  case_num  ENV  System  title  details  result  time_consuming\n' \
                     + '-------------------------------------------------------\n'
        testdata = ''
        for i in range(0, alltest_count):
            alltestdef = alltestdef + self.iTestSuite[i]['successes'] + self.iTestSuite[i]['failures']+self.iTestSuite[i]['errors']+self.iTestSuite[i]['skipped']
            rul = 'Pass_%d Fail_%d' % (self.iTestSuite[i]['successes'],self.iTestSuite[i]['failures']+self.iTestSuite[i]['errors'])
            '''
            rul = '_'
            if self.iTestSuite[i]['run'] == self.iTestSuite[i]['successes']:
                rul = 'Pass'
            if self.iTestSuite[i]['failures'] > 0:
                rul = 'Failures'
            if self.iTestSuite[i]['errors'] > 0:
                rul = 'Error'
            if self.iTestSuite[i]['skipped'] > 0:
                rul = 'Skipped'
            '''
            if i != 0:
                testdata = testdata + '\n'
            testdata = testdata + str(self.all_type_to_encode(i)) + '  ' \
                       + self.all_type_to_encode(self.iTestSuite[i]['case_num']) + '  ' \
                       + self.all_type_to_encode(self.iTestSuite[i]['environment']) + '  ' \
                       + self.all_type_to_encode(self.iTestSuite[i]['subsystem']) + '  ' \
                       + self.all_type_to_encode(self.iTestSuite[i]['title']) + '  ' \
                       + self.all_type_to_encode(self.iTestSuite[i]['details']) + '  ' \
                       + self.all_type_to_encode(rul) + '  ' \
                       + str(int(self.iTestSuite[i]['time_consuming']))+ 'sec'
            if int(self.iTestSuite[i]['run']) > 1:
                trdetail = ''
                if self.iTestSuite[i]['failures'] > 0:
                    for fail in self.iTestSuite[i]['failures_str']:
                        trdetail = trdetail + '\n\t  ' + str(fail[0].test_id) + '  failures'
                        # trdetail = trdetail + fail[1]  # track message
                if self.iTestSuite[i]['errors'] > 0:
                    for error in self.iTestSuite[i]['errors_str']:
                        trdetail = trdetail + '\n\t  ' + str(error[0].test_id) + ' errors'
                        # trdetail = trdetail + error[1]  # track message
                if self.iTestSuite[i]['skipped'] > 0:
                    for skip in self.iTestSuite[i]['skipped_str']:
                        trdetail = trdetail + '\n\t  ' + str(skip[0]) + ' skipped'
                        # trdetail = trdetail + skip[1]  # track message
                if self.iTestSuite[i]['successes'] > 0:
                    for succ in self.iTestSuite[i]['successes_str']:
                        trdetail = trdetail + '\n\t  ' + str(succ.test_id) + ' pass'
                trdetail = self.codetocnstr(trdetail)
                testdata = testdata + self.all_type_to_encode(trdetail)

        report_str = report_str + testdata + '\n-------------------------------------------------------\n'
        durtime = int(self.endtime - self.starttime)
        if durtime > 3600:
            durtimestr = str(durtime / 3060) + ' h ' + str((durtime % 3600) / 60) + ' min ' + str(
                (durtime % 3600) % 60) + ' sec'
        elif durtime > 60:
            durtimestr = str(durtime / 60) + ' min ' + str(durtime % 60) + ' sec'
        else:
            durtimestr = str(durtime) + ' sec'
        report_str = report_str + 'Total:' + str(alltestdef) + ' | time consuming:' + durtimestr
                     #+ str(durtime / 60) + ' min ' + str(durtime % 60) + ' sec\n'
        #print report_str
        return report_str

    def write_txt(self, filename, datatxt):
        file_object = open(filename, 'w')
        try:
            file_object.write(datatxt)
        finally:
            file_object.close()

    def removeFileInFirstDir(self, targetDir):
        for file in os.listdir(targetDir):
            targetFile = os.path.join(targetDir, file)
            if os.path.isfile(targetFile):
                os.remove(targetFile)

    def codetocnstr(self, str):
        if str.find('_x') != -1:
            reStr = re.compile(r'_x..')
            findallstr = reStr.findall(str)
            if len(findallstr) != 0:
                for i in findallstr:
                    tmp = i.replace('_x', '\\x')
                    try:
                        str = str.replace(i, tmp.decode('string_escape'))
                    except:
                        str = str.replace(i, tmp)
        if str.find('_u') != -1:
            str = str.replace('_u_', '_')
            reStr = re.compile(r'_u....')
            findallstr = reStr.findall(str)
            if len(findallstr) != 0:
                for i in findallstr:
                    tmp = i.replace('_u', '\u')
                    try:
                        tmp = tmp.decode('unicode-escape')
                    except Exception as e:
                        print e
                    str = str.replace(i, tmp)
        return str

    # 按系统和环境统计数据，统计每个环境下，每个系统运行测试通过数、失败数、跳过数的合计
    def Env_Sys_TongJi(self):
        rultList = [
            # {'ENV': 'STG', 'System': 'XN', 'successes': 10, 'errors':2 , 'failures':2, 'skipped':2}
        ]
        for iTestCase in self.iTestSuite:
            flag = False
            for rult in rultList:
                if iTestCase['environment'] == rult['environment'] and iTestCase['subsystem'] == rult['subsystem']:
                    rult['successes'] = rult['successes'] + iTestCase['successes']
                    rult['errors'] = rult['errors'] + iTestCase['errors']
                    rult['failures'] = rult['failures'] + iTestCase['failures']
                    rult['skipped'] = rult['skipped'] + iTestCase['skipped']
                    flag = True
                    break
            if flag == False:
                tmp = {}
                tmp['environment'] = iTestCase['environment']
                tmp['subsystem'] = iTestCase['subsystem']
                tmp['successes'] = iTestCase['successes']
                tmp['errors'] = iTestCase['errors']
                tmp['failures'] = iTestCase['failures']
                tmp['skipped'] = iTestCase['skipped']
                rultList.append(tmp)
                # print 'has_key',dict.has_key('ENV')
                # print 'in','ENV' in dict.keys()
        return rultList

if __name__ == '__main__':
    whtml = CreateHtmlReport()
    print str(int(whtml.all_type_to_encode(0.00100016593933)))
    whtml.iTestSuite = [
{'errors': 0, 'run': 6, 'title': 'title test case', 'successes': 3, 'start_time': 1465717564.637,
    'skipped_str': [('<xmlrunner.result._TestInfo object at 0x000000000273C8D0>', 'demonstrating skipping')],
	'failures_str': [('<xmlrunner.result._TestInfo object at 0x000000000273C5C0>', 'Traceback (most recent call last):\n  File "D:\\PythonWorks\\MyPyTestOne\\stu_unitest\\junitreport.py", line 35, in test_failed\n    self.assertEqual(1,2)\nAssertionError: 1 != 2\n'),
	                 ('<xmlrunner.result._TestInfo object at 0x00000000027CB828>', 'Traceback (most recent call last):\n  File "D:\\PythonWorks\\MyPyTestOne\\stu_unitest\\junitreport.py", line 38, in test_failed2\n    self.assertEqual(3, 2)\nAssertionError: 3 != 2\n'),
	                 ('<xmlrunner.result._TestInfo object at 0x000000000273C780>', 'Traceback (most recent call last):\n  File "D:\\PythonWorks\\MyPyTestOne\\stu_unitest\\junitreport.py", line 41, in test_failed2\n    self.assertEqual(13, 12)\nAssertionError: 13 != 12\n')],
	'errors_str': [], 'skipped': 1, 'details': 'test case details', 'failures': 3, 'time_consuming': 0.0, 'stop_time': 1465717564.637},
{'errors': 0, 'run': 3, 'title': 'title test case', 'successes': 3, 'start_time': 1465717564.649, 'skipped_str': [], 'failures_str': [], 'errors_str': [], 'skipped': 0, 'details': 'test case details', 'failures': 0, 'time_consuming': 2.001000165939331, 'stop_time': 1465717566.65}
]
    #whtml.create_html_report()
    whtml.removeFileInFirstDir(sys.path[0] + '/output')
