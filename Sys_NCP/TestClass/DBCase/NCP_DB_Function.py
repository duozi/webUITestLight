#coding=utf-8
import sys,time,unittest,xmlrunner,os
from Sys_NCP.PageObj.NCPTest import NCPTest

class NCP_DB_Function(unittest.TestCase):
    '''合同查询 '''
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    actdb = None  # 接收main脚本传送的mysql处理类对象
    row = ""  # 接收main脚本传送的当前处理的行数(测试数据list的index号，从0开始)
    logstu = ""  # 接收main脚本传递来的写log的对象
    Screenshotfilepath = "" #接收本轮截屏文件保存路径
    s = os.sep
    test = ""

    def setUp(self):
        pass
    def testCountManage(self):
        self.contractQuery()

    def contractQuery(self):
        self.test = NCPTest()
        self.test.login(self.dict_data["登录用户"], self.dict_data["登录密码"],self.dict_data["登录地址"])
        self.test.go_to_menu(self.dict_data["一级菜单"], self.dict_data["二级菜单"])
        for i in range(0,6):
            str1 = "查询条件"+str(i+1)
            if self.dict_data[str1]<>'':
                self.logstu.info (u'查询参数为：%s'%self.dict_data[str1])
                QueryInfo = self.dict_data[str1].split("|")
                if QueryInfo[0] == '1' and len(QueryInfo)>=3:
                    if len(QueryInfo) == 4 and QueryInfo[3] == 'by_Prompt':
                        self.test.input_by_placeholder(QueryInfo[1], QueryInfo[2])
                    elif len(QueryInfo) == 4 and QueryInfo[3] == 'by_id':
                        self.test.input_by_id(QueryInfo[1], QueryInfo[2])
                    elif len(QueryInfo) == 3:
                        self.test.input_by_placeholder(QueryInfo[1], QueryInfo[2])
                    else:
                        print (u'输入参数格式不正确，请检查')
                        pass
                elif QueryInfo[0] == '2' and len(QueryInfo)>=3:
                    if len(QueryInfo) == 3:
                        self.test.select_option_value(QueryInfo[1], QueryInfo[2])
                    elif len(QueryInfo) == 4 and QueryInfo[3] == 'by_id':
                        self.test.select_option_value(QueryInfo[1], QueryInfo[2])
                    else:
                        print (u'输入参数格式不正确，请检查')
                        pass
                elif QueryInfo[0] == '3':
                    self.test.select_calendar_byId(QueryInfo[1], QueryInfo[2])
                else:
                    print (u'输入参数格式不正确，请检查')
        self.test.click_button(self.dict_data["操作类型"])
        self.Screenshotfilepath = self.Screenshotfilepath+self.s+'NCP'
        self.test.saveScreenshot_Path(self.dict_data["案例详情"],self.Screenshotfilepath) #滚动前截图
        # elem_id = ''
        self.test.scroll_saveScreenshot_Path(self.dict_data["案例详情"],self.Screenshotfilepath) #滚动后截图

        time.sleep(3)
        self.test.close_tab('合同查询')
        self.test.browserquit()
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)