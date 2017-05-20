#coding=utf-8
import sys,time,unittest,xmlrunner,os
from Sys_NCP.PageObj.NCPTest import NCPTest
from Utils.scriptTestCase import scriptTestCase

class ContractQuery_CombinationCondition(unittest.TestCase):
    '''合同管理>合同查询>查询功能-组合条件查询 '''
    Screenshotfilepath = ""  # 接收本轮截屏文件保存路径
    s = os.sep
    sTC = scriptTestCase()

    def setUp(self):
        pass
    def testCountManage(self):
        test = NCPTest()
        self.Screenshotfilepath = test.get_check_filepath(self.Screenshotfilepath)
        testdatas = self.sTC.get_ContractQuery_CombinationConditionTestData()
        # test.login('admin', '88888888')
        test.defaultLoginInfo()
        for i in range(0,len(testdatas)):
            test.go_to_menu('合同管理', '合同查询')
            if testdatas[i]['QueryMethod'] == 'CombinationCondition':
                countValues = testdatas[i]['LocationValue'].split(',')
                for j in range(0,len(countValues)):
                    Queryvalue = countValues[j].split('|')
                    if Queryvalue[0] == '输入框提示':
                        test.input_by_placeholder(Queryvalue[1], Queryvalue[2])
                    elif  Queryvalue[0] == '输入框id':
                        test.input_by_id(Queryvalue[1], Queryvalue[2])
                    elif Queryvalue[0] == '下拉选择框id':
                        test.select_option_value(Queryvalue[1], Queryvalue[2])
                    elif Queryvalue[0] == '日期输入框id':
                        test.select_calendar_byId(Queryvalue[1], Queryvalue[2])
                    elif Queryvalue[0] == '日期输入框提示':
                        test.select_calendar_byId(Queryvalue[1], Queryvalue[2])
                    else:
                        print (u'输入参数格式不正确，请检查')
            else:
                print (u'输入参数格式不正确，请检查')
            test.click_button('搜索')
            test.saveScreenshot_Path(testdatas[i]['截图名称'], self.Screenshotfilepath)  # 滚动前截屏
            test.scroll_saveScreenshot_Path(testdatas[i]['截图名称'], self.Screenshotfilepath, "tablelist")  # 滚动后截屏
            time.sleep(3)
            test.close_tab('合同查询')

        test.driver.quit()
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)