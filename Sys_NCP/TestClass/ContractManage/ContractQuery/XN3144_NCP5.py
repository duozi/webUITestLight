#coding=utf-8
import sys,time,unittest,xmlrunner,os
from Sys_NCP.PageObj.NCPTest import NCPTest
from Utils.scriptTestCase import scriptTestCase

class checkMainPageElement(unittest.TestCase):
    '''合同管理>合同查询>验证主界面的界面元素 '''
    Screenshotfilepath = ""  # 接收本轮截屏文件保存路径
    s = os.sep
    sTC = scriptTestCase()
    def setUp(self):
        pass
    def testCountManage(self):
        test = NCPTest()
        self.Screenshotfilepath = test.get_check_filepath(self.Screenshotfilepath)
        testdatas = self.sTC.get_checkMainPageElementTestData()

        # test.login('admin', '88888888') # 登录系统
        test.defaultLoginInfo()

        for i in range(0,len(testdatas)):
            # test.go_to_menu('合同管理','合同查询')
            print testdatas[i]['menuName_one']+','+testdatas[i]['menuName_two']
            # test.go_to_menu(testdatas[i]['menuName_one'], testdatas[i]['menuName_two'])
            if testdatas[i]['LocationMethod'] == '页面元素名称':
                test.checkElementByText(testdatas[i]['LocationValue'])
            elif testdatas[i]['LocationMethod'] == '页面元素id':
                test.checkElementByTextById(testdatas[i]['LocationValue'])
            else:
                print (u'输入参数格式不正确，请检查')
                pass
            test.saveScreenshot_Path(testdatas[i]['截图名称'], self.Screenshotfilepath)  # 滚动前截屏
            time.sleep(3)
            test.close_tab(testdatas[i]['menuName_two'])

        test.driver.quit()
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)