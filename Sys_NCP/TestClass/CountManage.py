#coding=utf-8
import sys,time,unittest,xmlrunner,os

from Sys_NCP.PageObj.NCPTest import NCPTest


class CountManage(unittest.TestCase):
    Screenshotfilepath = ""  # 接收本轮截屏文件保存路径
    s = os.sep
    def setUp(self):
        pass
    def testCountManage(self):
        test = NCPTest()
        self.Screenshotfilepath = test.get_check_filepath(self.Screenshotfilepath)
        # test.login('admin', '88888888')
        test.defaultLoginInfo()
        test.go_to_menu('账户管理', '账户综合信息查询')
        test.input_by_placeholder('账户名称', '中山市横栏镇伟昌摩托车销售商行')
        test.click_button('搜索')
        # test.save_screenshot()
        test.saveScreenshot_Path('账户管理_账户综合信息查询1', self.Screenshotfilepath)
        time.sleep(3)
        test.close_tab('账户综合信息查询')
        test.go_to_menu('账户管理', '现金账户信息管理')
        # test.input_by_id('p_accountName', '易鸣')
        # test.input_by_id('accountNo', 'PT20161104000000502657')
        test.input_by_placeholder('账户名称', '易鸣')
        test.input_by_placeholder('账户号', 'PT20161104000000502657')
        test.select_value('账户类别', '个人')
        test.click_button('搜索')
        # test.save_screenshot()
        test.saveScreenshot_Path('账户管理_现金账户信息管理1', self.Screenshotfilepath)
        time.sleep(3)
        test.action('查看流水')
        # test.save_screenshot()
        test.saveScreenshot_Path('账户管理_现金账户信息管理_查看流水1', self.Screenshotfilepath)
        time.sleep(5)
        test.close_sub_window()
        time.sleep(3)
        test.click_button('重置')
        test.input_by_placeholder('账户名称', '黄燕')
        test.click_button('搜索')
        # test.input_date_by_placeholder('开始日期','2016-11-01')
        # test.input_date_by_placeholder('结束日期', '2016-12-01')
        # test.click_button('搜索')
        # #调用日历选择封装方法
        # test.switch_to_latest_frame()
        # test.select_calendar('datemin','2016-11-01')
        # test.select_calendar('datemax', '2016-12-01')
        # test.Push_Enter()
        # test.driver.switch_to.default_content()
        ###
        # #调用获取table中某个单元格中的值
        table_ths1 = test.get_tableCell_value(0,3)
        print table_ths1
        # test.save_screenshot()
        # test.saveScreenshot_Path('账户管理_日期查询1', self.Screenshotfilepath)

        test.driver.quit()
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
