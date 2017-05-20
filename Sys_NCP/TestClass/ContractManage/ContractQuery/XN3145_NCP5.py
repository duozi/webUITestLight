#coding=utf-8
import sys,time,unittest,xmlrunner,os
from Sys_NCP.PageObj.NCPTest import NCPTest
from Utils.scriptTestCase import scriptTestCase

class checkContractQueryPageElement(unittest.TestCase):
    '''合同管理>合同查询>查看合同查询页面 '''
    Screenshotfilepath = ""  # 接收本轮截屏文件保存路径
    s = os.sep
    sTC = scriptTestCase()
    def setUp(self):
        pass
    def testCountManage(self):
        test = NCPTest()
        self.Screenshotfilepath = test.get_check_filepath(self.Screenshotfilepath)
        testdatas = self.sTC.get_checkPageElementTestData()
        # test.login('admin', '88888888') # 登录系统
        test.defaultLoginInfo()
        for i in range(0,len(testdatas)):
            test.go_to_menu(testdatas[i]['menuName_one'],testdatas[i]['menuName_two'])
            TexvtValues = testdatas[i]['LocationValue'].split(',')
            exitTextValues = ''
            notexitTextValues = ''
            test.switch_to_latest_frame()
            for j in range(0, len(TexvtValues)):
                # returnValue = test.checkElementTextByButton(buttonTexvtValues[j])
                returnValue = test.checkElementText(testdatas[i]['LocationMethod'], TexvtValues[j])
                if returnValue == 'true':
                    exitTextValues = exitTextValues + TexvtValues[j] + ','
                else:
                    notexitTextValues = notexitTextValues + TexvtValues[j] + ','
            print u'%s:\'%s\'存在' % (testdatas[i]['截图名称'],exitTextValues)
            test.saveScreenshot_Path(testdatas[i]['截图名称'], self.Screenshotfilepath)  # 滚动前截屏
            time.sleep(3)
            test.close_tab(testdatas[i]['menuName_two'])
        if notexitTextValues <> '':
            print u'%s:\'%s\'不存在，案例运行失败' % (testdatas[i]['截图名称'],notexitTextValues)
            self.assertEqual(notexitTextValues, '')

        test.driver.quit()
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)