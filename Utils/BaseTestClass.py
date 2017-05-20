#!/usr/bin/python
# -*- coding: UTF-8 -*-
import unittest,xmlrunner,sys,logging,datetime,os
from WebDriver_Normal import WebDriver_Normal
from WebUITestLight.Utils.logger import Logger
from WebUITestLight.Utils.UnitTestRultAct import UnitTestRultAct
import traceback
reload(sys)
sys.setdefaultencoding('utf8')

class BaseTestClass(unittest.TestCase):
    log = Logger()
    browserclass = None #WebDriver_Normal('Chrome')
    # browserclass = ""  # WebDriver_Normal('Chrome')
    # cls.driver = '' #接收传送过来的driver

    @classmethod
    def setUpClass(cls):
        '''
        测试类中所有测试方法执行前执行的方法
            这里做了UI自动化测试浏览器初始化工作
        :return:
        '''
        cls.log.info("Hook method for setting up class fixture before running tests in the class.")
        # cls.browserclass = WebDriver_Normal('Chrome')
        # print cls.driver
        try:
            if cls.driver <>"" or cls.driver <>None:
                browserName = cls.driver
        except Exception as e:
            browserName = 'Firefox'
        finally:
            cls.browserclass = WebDriver_Normal(browserName)

    @classmethod
    def tearDownClass(cls):
        '''
        测试类中所有方法执行完毕后执行的方法
            关闭所有的浏览器
        :return:
        '''
        cls.log.info( "Hook method for tear Down  class fixture before running tests in the class.")
        cls.browserclass.quit_driver()

    def onTestFailure(self, imgfileprefix='err'):
        '''
        测试方法执行失败触发的方法
        :return: 在报告中显示的内容
        '''
        try:
            imgname = '%s%s.png' % (imgfileprefix,datetime.datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3])
            imgpath = sys.path[0] + '/output/images/'
            if os.path.exists(imgpath) == False:
                os.makedirs(imgpath)
            imgfile = imgpath + imgname
            self.browserclass.get_driver().get_screenshot_as_file(imgfile)
            htmlimg = '<br><img src="images/' + imgname + '" width="800" ><br>'
            return imgfile, htmlimg
        except:
            return traceback.format_exc()


if __name__ == '__main__':
    # 自定义 html 报告 txt 报告 xml报告
    suite = unittest.makeSuite(BaseTestClass)
    testRunner = xmlrunner.XMLTestRunner(output=sys.path[0] + '/output')
    testRunner.failfast = False
    testRunner.buffer = False
    testRunner.catchbreak = False
    var = testRunner.run(suite)
    caserult = UnitTestRultAct()
    caserult.CreateReport([caserult.get_TestCase(var)], strcode='gbk')


    ''' # xml 报告
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output=sys.path[0] + '/output'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)
    '''