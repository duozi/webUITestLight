#coding=utf-8
import sys,time,unittest,xmlrunner,os
from Sys_NCP.PageObj.NCPTest import NCPTest

class SingleConditionQuery(unittest.TestCase):
    '''合同管理>合同查询>查询功能-组合条件查询 '''
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
    def testSingleConditionQuery(self):
        test = NCPTest()
        self.Screenshotfilepath = test.get_check_filepath(self.Screenshotfilepath)
        # test.login('admin', '88888888')
        test.defaultLoginInfo()

        test.go_to_menu(self.dict_data["一级菜单"], self.dict_data["二级菜单"])
        QueryUnsuccessfulInfo = ''
        test.switch_to_latest_frame()
        for i in range(0, 6):
            str1 = "查询条件" + str(i + 1)
            if self.dict_data[str1] <> '':
                self.logstu.info(u'检查参数为：%s' % self.dict_data[str1])
                Queryvalue = self.dict_data[str1].split("|")
                if Queryvalue[0] == '输入框提示':
                    test.input_by_placeholder(Queryvalue[1], Queryvalue[2])
                    break
                elif Queryvalue[0] == '输入框id':
                    test.input_by_id(Queryvalue[1], Queryvalue[2])
                    break
                elif Queryvalue[0] == '下拉选择框id':
                    test.select_option_value(Queryvalue[1], Queryvalue[2])
                    break
                elif Queryvalue[0] == '日期输入框id':
                    test.select_calendar_byId(Queryvalue[1], Queryvalue[2])
                    break
                elif Queryvalue[0] == '日期输入框提示':
                    test.select_calendar_byId(Queryvalue[1], Queryvalue[2])
                    break
                else:
                    QueryUnsuccessfulInfo = '参数格式不正确'
        for i in range(0, 40):
            str1 = "输入值" + str(i + 1)
            if self.dict_data[str1] <> '':
                self.logstu.info(u'查询参数为：%s' % self.dict_data[str1])
                Queryvalue = self.dict_data[str1].split("|")
                if Queryvalue[0] == '输入框提示':
                    test.input_by_placeholder(Queryvalue[1], Queryvalue[2])
                    break
                elif Queryvalue[0] == '输入框id':
                    test.input_by_id(Queryvalue[1], Queryvalue[2])
                    break
                elif Queryvalue[0] == '下拉选择框id':
                    test.select_option_value(Queryvalue[1], Queryvalue[2])
                    break
                elif Queryvalue[0] == '日期输入框id':
                    test.select_calendar_byId(Queryvalue[1], Queryvalue[2])
                    break
                elif Queryvalue[0] == '日期输入框提示':
                    test.select_calendar_byId(Queryvalue[1], Queryvalue[2])
                    break
                else:
                    QueryUnsuccessfulInfo = '参数格式不正确'
        if QueryUnsuccessfulInfo <> '':
            Screenshotfilename = '_案例失败_'+self.dict_data["案例详情"]
            test.saveScreenshot_Path(Screenshotfilename, self.Screenshotfilepath)  # 滚动前截屏
            self.logstu.info(u'查询%s，案例运行失败' % (QueryUnsuccessfulInfo))
            self.assertEqual('1', '')
        else:
            test.click_button('搜索')
            time.sleep(3)
            test.saveScreenshot_Path(self.dict_data["案例详情"], self.Screenshotfilepath)  # 滚动前截屏
            test.scroll_saveScreenshot_Path(self.dict_data["案例详情"], self.Screenshotfilepath, "tablelist")  # 滚动后截屏
        time.sleep(3)
        test.close_tab(self.dict_data["二级菜单"])

        # for i in range(0,len(testdatas)):
        #     test.go_to_menu('合同管理', '合同查询')
        #     if testdatas[i]['LocationClass'] == '输入框':
        #         if testdatas[i]['LocationMethod'] == '输入框提示':
        #             test.input_by_placeholder(testdatas[i]['LocationValue'],testdatas[i]['FillingValue'])
        #         elif testdatas[i]['LocationMethod'] == '输入框id':
        #             test.input_by_id(testdatas[i]['LocationValue'], testdatas[i]['FillingValue'])
        #         else:
        #             print (u'输入参数格式不正确，请检查')
        #             pass
        #     elif testdatas[i]['LocationClass'] == '下拉选项':
        #         if testdatas[i]['LocationMethod'] == '输入框id':
        #             test.select_option_value(testdatas[i]['LocationValue'], testdatas[i]['FillingValue'])
        #         elif testdatas[i]['LocationMethod'] == '输入框提示':
        #             test.select_option_value(testdatas[i]['LocationValue'], testdatas[i]['FillingValue'])
        #         else:
        #             print (u'输入参数格式不正确，请检查')
        #             pass
        #     elif testdatas[i]['LocationClass'] == '日期':
        #         if testdatas[i]['LocationMethod'] == '输入框id':
        #             test.select_calendar_byId(testdatas[i]['LocationValue'], testdatas[i]['FillingValue'])
        #         elif testdatas[i]['LocationMethod'] == '输入框提示':
        #             test.select_calendar_byId(testdatas[i]['LocationValue'], testdatas[i]['FillingValue'])
        #         else:
        #             print (u'输入参数格式不正确，请检查')
        #             pass
        #     else:
        #         print (u'输入参数格式不正确，请检查')
        #     test.click_button('搜索')
        #     test.saveScreenshot_Path(testdatas[i]['截图名称'], self.Screenshotfilepath)  # 滚动前截屏
        #     test.scroll_saveScreenshot_Path(testdatas[i]['截图名称'], self.Screenshotfilepath, "tablelist")  # 滚动后截屏
        #     time.sleep(3)
        #     test.close_tab('合同查询')
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)