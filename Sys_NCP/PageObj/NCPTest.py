# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from Utils.lyFunction import PubFunction
import time,sys,os

class NCPTest():
    s = os.sep
    pubNcp = PubFunction()
    def __init__(self):
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.autosavescreen = False
        argv0_list = sys.argv[0].split("/");
        self.script_name = argv0_list[len(argv0_list) - 1]
        self.script_name = self.script_name[0:-3]
        # self.folder = "Screenshot/%s%s" % (self.script_name, time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        # self.folder = "%s%s" % (self.script_name, time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        self.folder = sys.path[0] + self.s + 'Screenshot' #+ self.s+time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        # print self.folder
        # os.makedirs(self.folder)

    def __del__(self):
        self.driver.close()

    def set_auto_screenshot(self, value):
        self.autosavescreen = value

    def login(self, username, psw,login_url_in=None):
        if login_url_in == None:
            login_url = 'http://10.18.12.15:8080/ncp-web/pages/login.jsp'
        else:
            login_url = login_url_in
        # self.driver.get('http://10.18.12.15:8080/ncp-web/pages/login.jsp')
        self.driver.get(login_url)
        elem = self.driver.find_element_by_id("loginname")
        elem.clear()
        elem.send_keys(username)
        elem = self.driver.find_element_by_id("password")
        elem.clear()
        elem.send_keys(psw)
        elem = self.driver.find_element_by_name("登录")
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException as e:
            print("no alert in login")
        self.auto_save_screen()
    def defaultLoginInfo(self):
        self.login('admin', '88888888')

    def auto_save_screen(self):
        if self.autosavescreen:
            time.sleep(1)
            self.save_screenshot()

    def logout(self):
        '''elem = self.driver.find_element_by_link_text('退出系统')
        elem.click()
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException as e:
            print("no alert in logout")'''
        pass

    def go_to_menu(self, menu, submenu):
        time.sleep(1)
        find = False
        for elem in self.driver.find_elements_by_tag_name('dl'):
            if elem.text.find(self.try_to_unicode(menu)) >= 0:
                if elem.find_element_by_tag_name('dt').get_attribute('class') != 'selected':
                    elem.click()
                for sublink in elem.find_elements_by_tag_name('li'):
                    if sublink.text == self.try_to_unicode(submenu):
                        sublink.click()
                        find = True
                        break
                break
        # if find is False:
        #     self.saveScreenshot_Path()
        # else:
        #     self.saveScreenshot_Path()
        frames = self.driver.find_elements_by_tag_name('iframe')
        self.frame = frames[1] #第二个frame为当前frame

    def save_screenshot(self, filename=None):
        if filename is None:
            filename = '%s.png' % time.strftime('%Y-%m-%d.%H%M%S',time.localtime(time.time()))
        filename = r'.\%s\%s' % (self.folder, filename)
        filepath = unicode(filename, 'utf8')
        self.driver.switch_to.default_content()
        self.driver.get_screenshot_as_file(filepath)
        self.driver.save_screenshot(filename)
        print filename
        print filepath

    def switch_to_latest_frame(self):
        if self.frame is not None:
            self.driver.switch_to.frame(self.frame)

    #切换到日期选择控件的frame
    def __switch_to_date_selection_frame(self):
        frames = self.driver.find_elements_by_tag_name('iframe')
        frame = frames[frames.__len__() - 1]
        self.driver.switch_to.frame(frame)

    def input_by_id(self, id, value):
        self.switch_to_latest_frame()
        elem = self.driver.find_element_by_id(id)
        elem.clear()
        elem.send_keys(unicode(value,'utf8'))
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    def input_by_placeholder(self, placeholder, value):
        self.switch_to_latest_frame()
        elem = self.driver.find_element_by_css_selector("input[placeholder=\"%s\"]" % self.try_to_unicode(placeholder))
        elem.clear()
        elem.send_keys(self.try_to_unicode(value))
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    def input_date_by_placeholder(self, placeholder, date):
        self.switch_to_latest_frame()
        elem = self.driver.find_element_by_css_selector("input[placeholder=\"%s\"]" % unicode(placeholder,'utf8'))
        elem.clear()
        elem.send_keys(unicode(date, 'utf8'))
        elem.send_keys(Keys.TAB)
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    def input_date_by_id(self, id, date):
        self.switch_to_latest_frame()
        elem = self.driver.find_element_by_id(id)
        elem.clear()
        elem.send_keys(unicode(date, 'utf8'))
        elem.send_keys(Keys.TAB)
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    def click_button(self,name):
        name = self.try_to_unicode(name)
        self.switch_to_latest_frame()
        find = False
        for button in self.driver.find_elements_by_tag_name('button'):
            if button.text.find(name) >= 0:
                find = True
                button.click()
                break
        if find == False:
            for button in self.driver.find_elements_by_tag_name('a'):
                if button.text.find(name) >= 0:
                    find = True
                    button.click()
                    break
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    def action(self, action):
        action = self.try_to_unicode(action)
        self.switch_to_latest_frame()
        for button in self.driver.find_elements_by_tag_name('a'):
            if button.get_attribute('title').find(action) >= 0:
                button.click()
                break
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    def close_sub_window(self):
        self.switch_to_latest_frame()
        self.driver.find_element_by_class_name('layui-layer-setwin').click()
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    def close_tab(self, name):
        name = self.try_to_unicode(name)
        head = self.driver.find_element_by_id('min_title_list')
        for tab in head.find_elements_by_tag_name('li'):
            if tab.find_element_by_tag_name('span').text.find(name) >= 0:
                tab.find_element_by_tag_name('i').click()
                break
        self.auto_save_screen()

    def select_value(self, key, value):
        self.switch_to_latest_frame()
        for span in self.driver.find_elements_by_tag_name('span'):
            if span.text.find(self.try_to_unicode(key)) >= 0:
                for option in span.find_elements_by_tag_name('option'):
                    if option.text.find(self.try_to_unicode(value)) >= 0:
                        option.click()
                        break
                break
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    def turn_to_page(self, page):
        self.switch_to_latest_frame()
        div = self.driver.find_element_by_class_name('pagination')
        for link in div.find_elements_by_tag_name('div'):
            if link.text == unicode(page, 'utf8'):
                link.click()
                break
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    #选中列表前面的复选框
    def select_table_item(self, column, value):
        column = self.try_to_unicode(column)
        value = self.try_to_unicode(value)
        self.switch_to_latest_frame()
        table = self.driver.find_element_by_css_selector("table[id=\"tablelist\"]")
        head = table.find_element_by_tag_name('thead')
        index = 0
        for col in head.find_elements_by_tag_name('th'):
            if col.text == column:
                break
            index = index + 1
        body = table.find_element_by_tag_name('tbody')
        for row in body.find_elements_by_tag_name('tr'):
            items = row.find_elements_by_tag_name('td')
            if items[index].text == value:
                items[0].click()
        self.driver.switch_to.default_content()
        self.auto_save_screen()

    # 日历通过元素id 调用方法_by zhuoshenghua
    def select_calendar(self, elem_id, date):
        self.driver.find_element_by_id(self.try_to_unicode(elem_id)).click()
        time.sleep(2)
        self.driver.switch_to.active_element.send_keys(self.try_to_unicode(date))
        time.sleep(2)
    def Push_Enter(self):
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)

    def select_calendar_byId(self, elem_id, date):
        self.switch_to_latest_frame()
        self.select_calendar(elem_id,date)
        self.Push_Enter()
        self.driver.switch_to.default_content()
    ###_by zhuoshenghua


    table_td = (By.CSS_SELECTOR, '#tablelist >tbody >tr')  # 标题th
    table_td2 = (By.CSS_SELECTOR, '#tablelist >thead >tr')  # 标题th 写法2
    # 封装获取table中某个单元格中的值，参数是行和列_by zhuoshenghua
    def get_tableCell_value(self, tableRow=None, tableColumn=None):
        tableRow = self.try_to_unicode(tableRow)
        tableColumn = self.try_to_unicode(tableColumn)
        self.switch_to_latest_frame()
        table_td = self.table_td
        table_td2 = self.table_td2
        table_ths = self.findAlls(6, *(table_td, table_td2))
        tableCellvalue = table_ths[tableRow].find_elements_by_tag_name('td')[tableColumn].text
        self.driver.switch_to.default_content()
        return tableCellvalue

    def findAlls(self, time_all, *ByValue):
        driver = self.driver
        if len(ByValue) < 1:
            return False
        for for_i in range(0, time_all):
            for bv in (ByValue):
                bvElements = driver.find_elements(*bv)
                if len(bvElements) > 0:
                    return bvElements
            time.sleep(1)
        raise Exception("NoSuchElementException findAlls find_elements:\n" + ByValue.__str__())
    ###_by zhuoshenghua

    # 封装截屏并保存截图文件方法，参数是文件名和文件路径_by zhuoshenghua
    def saveScreenshot_Path(self,filename=None,filepath=None):
        # filename = self.try_to_unicode(filename)
        # filepath = self.try_to_unicode(filepath)
        self.driver.switch_to.default_content()
        if filepath == None:
            filePath = self.get_check_filepath()
        else:
            filePath = filepath
        print filePath
        if os.path.exists(filePath):
            pass
            # print u'文件夹已存在'
        else:
            os.mkdir(filepath)
        if filename == None:
            FileName = '%s.png' % time.strftime('%H%M%S', time.localtime(time.time()))
        else:
            fileName = self.FileNameFilterConversion(filename)
            FileName =fileName+'_'+ '%s.png' % time.strftime('%H%M%S', time.localtime(time.time()))
        filePathName = filePath +self.s+ FileName
        self.driver.get_screenshot_as_file(self.try_to_unicode(filePathName))
        print filePathName

        # 封装滚动页面后（默认以id为tablelist为定点）截屏并保存截图文件方法，参数是文件名、文件路径和左上角定点id_by zhuoshenghua
    def scroll_saveScreenshot_Path(self, filename=None, filepath=None,elem_id=None):
        self.switch_to_latest_frame()
        if filename == None:
            FileName = '滚动后'
        else:
            FileName = filename + '_' + '滚动后'
        if elem_id == None:
            elem_id = 'tablelist'
        target = self.driver.find_element_by_id(elem_id)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        self.saveScreenshot_Path(FileName,filepath)

    def FileNameFilterConversion(self,content=None):
        str = ''
        if content ==None:
            print u'无需要检查转换的内容'
        else:
            for i in range(0,len(content)):
                if content[i] == ':' or content[i] == '\\' or content[i] == '/':
                    str = str
                else:
                    str = str + content[i]
        return str

    # 封装在当前路径下创建文件夹_by zhuoshenghua
    def Create_folder_current_path(self,folderName=None):
        if folderName ==None:
            folderPath = sys.path[0] + self.s + 'Screenshot'+ self.s + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        else:
            folderPath = sys.path[0] + self.s + 'Screenshot'+ self.s +folderName+ time.strftime('%H%M%S', time.localtime(time.time()))
        # print folderPath
        FolderName = self.try_to_unicode(folderPath)
        os.makedirs(FolderName)
        return folderPath
    ###_by zhuoshenghua

    def browserquit(self):
        self.driver.quit()

    def try_to_unicode(self, value):
        try:
            value = unicode(value, 'utf8')
        except Exception as e:
            # print e
            pass
        return value

    ###封装输入框通过id识别元素输入内容_by zhuoshenghua
    def input_by_id(self, id, value):
        self.switch_to_latest_frame()
        elem = self.driver.find_element_by_id(self.try_to_unicode(id))
        elem.clear()
        elem.send_keys(self.try_to_unicode(value))
        self.driver.switch_to.default_content()
        self.auto_save_screen()
    ### by zhuoshenghua

    ###封装选中下拉选项值，通过select的id和选项显示值识别元素选中内容_by zhuoshenghua
    def select_option_value(self, key, value):
        self.switch_to_latest_frame()
        for select in self.driver.find_elements_by_tag_name('select'):
            if select.get_attribute('id')== self.try_to_unicode(key):
                for option in select.find_elements_by_tag_name('option'):
                    if option.text.find(self.try_to_unicode(value)) >= 0:
                        option.click()
                        break
                break
        self.driver.switch_to.default_content()
        ### by zhuoshenghua

    ###封装 截屏文件保存文件夹生成_by zhuoshenhua
    def get_check_filepath(self,filepath=None):
        if filepath == ''or filepath == None:
            filepath = self.pubNcp.Create_folder_current_path()
        else:
            filepath = filepath
        return filepath
    ### by zhuoshenghua

    ###封装 读取配置文件的数据_by zhuoshenhua
    # def get_data(self,fileName=None,paragraphName=None,fieldName=None):
    #     projectPath = self.pubNcp.get_projectPath()
    #     filePathName = projectPath+fileName
    #     if fileName<>None and fieldName <> '':
    #         cf = ConfigParser.ConfigParser()
    #         cf.read(filePathName)
    #     if paragraphName<>None and paragraphName <> '' and fieldName<>None and fieldName <> '':
    #         data = cf.get(paragraphName,fieldName)
    #     return data
    # ### by zhuoshenghua

    def checkElementByText(self,LocationValue=None):
        # self.switch_to_latest_frame()
        if LocationValue <> None and LocationValue <> '':
            self.driver.file_detector_context(LocationValue)
        self.driver.switch_to.default_content()

    def checkElementByTextById(self,LocationValue=None):
        # self.switch_to_latest_frame()
        if LocationValue <> None and LocationValue <> '':
            self.driver.find_element_by_id(LocationValue)
        self.driver.switch_to.default_content()

    # 封装检查页面span标签中字段名称是否存在，参数是要检查的字段名称_by zhuoshenghua
    def checkElementTextBySpan(self,checkValue=None):
        flag = 'false'
        if checkValue <> None and checkValue <> '':
            for span in self.driver.find_elements_by_tag_name('span'):
                if span.text.find(self.try_to_unicode(checkValue)) >= 0:
                    flag = 'true'
                    break
            return flag
        self.driver.switch_to.default_content()
    ###

    # 封装检查页面table标签中标题字段名称是否存在，参数是要检查的标题字段名称_by zhuoshenghua
    def checkElementTextByTh(self, checkValue):
        flag = 'false'
        if checkValue <> None and checkValue <> '':
            for th in self.driver.find_elements_by_tag_name('th'):
                if th.text.find(self.try_to_unicode(checkValue)) >= 0:
                    flag = 'true'
                    break
            return flag
        self.driver.switch_to.default_content()
        ###

    # 封装检查页面a标签中连接，参数是要检查的连接字段名称_by zhuoshenghua
    def checkElementTextByA(self, checkValue):
        self.switch_to_latest_frame()
        # flag = 'false'
        if checkValue <> None and checkValue <> '':
            for th in self.driver.find_elements_by_tag_name('a'):
                if th.text.find(self.try_to_unicode(checkValue)) >= 0:
                    # flag = 'true'
                    th.click()
                    break
            # return flag
        self.driver.switch_to.default_content()
        ###

    # 封装检查页面button标签中按钮字段名称是否存在，参数是要检查的按钮字段名称_by zhuoshenghua
    def checkElementTextByButton(self, checkValue):
        flag = 'false'
        if checkValue <> None and checkValue <> '':
            for th in self.driver.find_elements_by_tag_name('button'):
                if th.text.find(self.try_to_unicode(checkValue)) >= 0:
                    flag = 'true'
                    break
            return flag
        self.driver.switch_to.default_content()
        ###

    # 封装检查页面标签中名称是否存在，参数是要检查的字段名称_by zhuoshenghua
    def checkElementText(self,ByTag, checkValue):
        flag = 'false'
        if checkValue <> None and checkValue <> '':
            for th in self.driver.find_elements_by_tag_name(ByTag):
                if th.text.find(self.try_to_unicode(checkValue)) >= 0:
                    flag = 'true'
                    break
            return flag
        self.driver.switch_to.default_content()

    ### ,linkName=None
    def checkbox(self,rowNum=None):
        self.switch_to_latest_frame()
        if rowNum <> None and rowNum <> '':
            elem_id = 'tablelist'
            target = self.driver.find_element_by_id(elem_id)
            self.driver.execute_script("arguments[0].scrollIntoView();", target)
            self.driver.switch_to.default_content()
            contractNum = self.get_tableCell_value(rowNum,2)
            print contractNum
            self.switch_to_latest_frame()
            checkBox = self.driver.find_element_by_id(contractNum)
            checkBox.click()
        self.driver.switch_to.default_content()

    def checkboxByElementName(self, ElementName=None):
        self.switch_to_latest_frame()
        if ElementName <> None and ElementName <> '':
            checkBox = self.driver.find_element_by_name(ElementName)
            checkBox.click()
        self.driver.switch_to.default_content()


