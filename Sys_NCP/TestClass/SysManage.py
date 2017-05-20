#coding=utf-8
import sys,time,unittest,xmlrunner,os

from Sys_NCP.PageObj.NCPTest import NCPTest


class SysManage(unittest.TestCase):
    Screenshotfilepath = ""  # 接收本轮截屏文件保存路径
    s = os.sep
    def setUp(self):
        pass
    def testCase1(self):
        test = NCPTest()
        self.Screenshotfilepath = self.Screenshotfilepath + self.s + 'NCP'
        # test.login('admin', '88888888')
        test.defaultLoginInfo()
        test.go_to_menu('系统管理', '角色管理')
        test.input_by_placeholder('输入角色名称', '数据总监')
        test.click_button('搜索')
        test.save_screenshot()
        time.sleep(3)
        test.action('详情')
        # test.save_screenshot('screenshot.png')
        test.saveScreenshot_Path('系统管理_角色管理screenshot1', self.Screenshotfilepath)
        time.sleep(3)

        test.driver.quit()
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)