#coding=utf-8
import sys,time,unittest,xmlrunner,os
from Sys_NCP.PageObj.NCPTest import NCPTest
from Utils.scriptTestCase import scriptTestCase

class ContractQuery_FormOperation(unittest.TestCase):
    '''合同管理>合同查询>查询功能-组合条件查询 '''
    Screenshotfilepath = ""  # 接收本轮截屏文件保存路径
    s = os.sep
    sTC = scriptTestCase()

    def setUp(self):
        pass
    def testCountManage(self):
        test = NCPTest()
        self.Screenshotfilepath = test.get_check_filepath(self.Screenshotfilepath)
        testdatas = self.sTC.get_ContractQuery_FormOperationTestData()
        # test.login('admin', '88888888')
        test.defaultLoginInfo()

        for i in range(0,len(testdatas)):
            if testdatas[i]['OperationMethod'] == 'FormOperation':
                countValues = testdatas[i]['LocationValue'].split(',')
                for j in range(0,len(countValues)):
                    test.go_to_menu(testdatas[i]['menuName_one'], testdatas[i]['menuName_two'])
                    Queryvalue = countValues[j].split('|')
                    if Queryvalue[0] <> '' and Queryvalue[1] <> '':
                        print Queryvalue[0]
                        test.checkbox(int(Queryvalue[1]))
                        test.checkElementTextByA(Queryvalue[0])
                        time.sleep(3)
                        test.saveScreenshot_Path(testdatas[i]['menuName_two']+'_'+testdatas[i]['截图名称']+'_'+Queryvalue[0], self.Screenshotfilepath)  # 滚动前截屏
                        time.sleep(3)
                        test.close_tab('合同查询')
                    else:
                        print (u'输入参数格式不正确，请检查')
            else:
                print (u'输入参数格式不正确，请检查')

        test.driver.quit()
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)