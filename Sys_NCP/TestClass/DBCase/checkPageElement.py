#coding=utf-8
import sys,time,unittest,xmlrunner,os
from Sys_NCP.PageObj.NCPTest import NCPTest

class checkPageElement(unittest.TestCase):
    '''合同管理>合同查询>查看合同查询页面 '''
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
    logstu = ""  # 接收main脚本传递来的写log的对象
    Screenshotfilepath = ""  # 接收本轮截屏文件保存路径
    s = os.sep
    test = ""

    def setUp(self):
        pass

    def testCheckPageElement(self):
        test = NCPTest()
        self.Screenshotfilepath = test.get_check_filepath(self.Screenshotfilepath)
        # test.login('admin', '88888888') # 登录系统
        test.defaultLoginInfo()

        test.go_to_menu(self.dict_data["一级菜单"], self.dict_data["二级菜单"])
        exitTextValues = ''
        notexitTextValues = ''
        test.switch_to_latest_frame()
        for i in range(0, 6):
            str1 = "查询条件" + str(i + 1)
            if self.dict_data[str1] <> '':
                self.logstu.info(u'检查参数为：%s' % self.dict_data[str1])
                checkInfo = self.dict_data[str1].split("|")
                returnValue = test.checkElementText(checkInfo[0], checkInfo[1])
                if returnValue == 'true':
                    exitTextValues = exitTextValues + checkInfo[1] + ','
                else:
                    notexitTextValues = notexitTextValues + checkInfo[1] + ','
        for i in range(0, 40):
            str1 = "输入值" + str(i + 1)
            if self.dict_data[str1] <> '':
                self.logstu.info(u'检查参数为：%s' % self.dict_data[str1])
                checkInfo = self.dict_data[str1].split("|")
                returnValue = test.checkElementText(checkInfo[0], checkInfo[1])
                if returnValue == 'true':
                    exitTextValues = exitTextValues + checkInfo[1] + ','
                else:
                    notexitTextValues = notexitTextValues + checkInfo[1] + ','
        if notexitTextValues <> '':
            Screenshotfilename = '_案例失败_'+self.dict_data["案例详情"]
            test.saveScreenshot_Path(Screenshotfilename, self.Screenshotfilepath)  # 滚动前截屏
            self.logstu.info(u'检查项：%s不存在，案例运行失败' % (notexitTextValues))
            self.assertEqual('1', '')
        else:
            test.saveScreenshot_Path(self.dict_data["案例详情"], self.Screenshotfilepath)  # 滚动前截屏
        time.sleep(3)
        test.close_tab(self.dict_data["二级菜单"])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)