#coding=utf-8
import sys,time,unittest,xmlrunner,os
from Sys_NCP.PageObj.NCPTest import NCPTest


class ContractQuery(unittest.TestCase):
    '''合同查询 '''
    Screenshotfilepath = ""  # 接收本轮截屏文件保存路径
    s = os.sep

    def setUp(self):
        pass
    def testCountManage(self):
        test = NCPTest()
        #调用在当前路径下创建文件夹，参数是文件夹名称（可为空），参数为空时系统自动创建以时间戳为名字的文件夹_by zhuoshenghua
        self.Screenshotfilepath = test.get_check_filepath(self.Screenshotfilepath)
        ###
        # test.login('admin', '88888888')
        test.defaultLoginInfo()
        test.go_to_menu('合同管理', '合同查询')
        # # # #调用截屏并保存截图文件方法_by zhuoshenghua
        test.saveScreenshot_Path('合同查询', self.Screenshotfilepath) #滚动前截屏
        test.scroll_saveScreenshot_Path("合同查询", self.Screenshotfilepath, "tablelist")  # 滚动后截屏
        # ###
        test.input_by_placeholder('输入客户名称', '暴发户')
        test.click_button('搜索')
        # # # #调用截屏并保存截图文件方法_by zhuoshenghua
        test.saveScreenshot_Path('合同查询_客户名称查询1', self.Screenshotfilepath)#滚动前截屏
        elem_id = 'CONTRACT_STATUS_TYPE'
        test.scroll_saveScreenshot_Path("合同查询_客户名称查询1", self.Screenshotfilepath,elem_id)  # 滚动后截图
        # ###
        ### 下拉框选中选项值
        test.select_option_value('PRODUCT_TYPE', '商品贷')
        test.click_button('搜索')
        # ###

        # # # #调用截屏并保存截图文件方法_by zhuoshenghua
        # # test.saveScreenshot_Path()
        # # test.saveScreenshot_Path('合同查询_客户名称查询')
        # test.saveScreenshot_Path('合同查询_客户名称查询1', self.Screenshotfilepath)
        # # test.saveScreenshot_Path('d:/Screenshots/query')
        # ###
        # # test.save_screenshot()
        # # #调用日历选择封装方法
        # test.select_calendar_byId('INPUT_DATE_BEGIN','2016-11-01')
        # test.select_calendar_byId('INPUT_DATE_END', '2016-12-01')
        # test.click_button('搜索')
        # test.saveScreenshot_Path('合同查询_申请日期查询1', self.Screenshotfilepath)  # 滚动前截屏
        # ###
        # # #调用获取table中某个单元格中的值
        # table_ths1 = test.get_tableCell_value(0, 3)
        # print table_ths1
        # ###
        time.sleep(10)
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