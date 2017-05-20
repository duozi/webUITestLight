# -*- coding: UTF-8 -*-

import logging
import os
import sys
import threading
import time

from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException,WebDriverException
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from Sys_CBS.PageObj.getElements import LoginElement
from Utils.logger import Logger

reload(sys)
sys.setdefaultencoding('utf8')

class PublicAct():
    alertSleepTime = 1
    tmp = ''
    s = os.sep
    def __init__(self, driver):  # test_dict_data, comm
        self.driver = driver
        # self.dict_data = test_dict_data  # 接收excel用例参数
        self.logstu = Logger(sys.path[0] + self.s + 'logs'+self.s+'autotest.log', logging.DEBUG, logging.DEBUG)
        '''
        if (self.dict_data["登录用户"] != "" and self.dict_data["登录密码"] != ""):
            #self.driver = self.comm.get_browserdrvie('Chrome')
            # 调用单例模式的类，调用其方法创建一个新的driver对象
            b = DriverInit()
            b.driver_init()
            self.driver = b.driver
        #self.driver.implicitly_wait(5)
        print type(self.driver)
        '''

    # 查询条件（一般在iframe right或right->rightup下）
    filterIconPlus = (By.ID, 'FilterIconPlus')  # 查询按钮前的 + img按钮
    filterIconMinus = (By.ID, 'FilterIconMinus')  # 查询按钮前的 - img按钮
    # 查询条件所在表格, 名称在tr下的td[0], td[1]是select控件选择等于、以...开始等， td[2\3\4]需要判断是否输入框输入参数
    selectList1 = (By.CSS_SELECTOR, 'div#FilterArea >table >tbody >tr >td >div >table >tbody >tr')
    selectList2 = (By.CSS_SELECTOR, 'div#FilterArea >table >tbody >tr >td >table >tbody >tr')
    # 按钮列表，依次有 查询  清空  恢复  取消
    selectTabBtn = (By.CSS_SELECTOR, 'div#FilterArea >table >tbody >tr + tr >td >input')
    #标题按钮
    title_btn = (By.CSS_SELECTOR, 'a[title]')
    # 表格操作的公用方法
    xntable = (By.CSS_SELECTOR, 'div#tableContainer >table')  # 定位表格
    table_th = (By.CSS_SELECTOR, 'div#tableContainer >table >tbody >tr >th')  # 标题th
    table_th2 = (By.CSS_SELECTOR, 'div#tableContainer >table >thead >tr >th')  # 标题th 写法2
    table_tr = (By.CSS_SELECTOR, 'div#tableContainer >table >tbody >tr')  # 表格所有行数
    table_td = (By.CSS_SELECTOR, 'div#tableContainer >table >tbody >tr >td')  # 表格所有的单元格
    table_btn = (By.CSS_SELECTOR, 'div.btn_text')  # 表格上的按钮 新增、详情、确认等
    table_btn2 = (By.CSS_SELECTOR, 'input[type="button"]')  # 表格下的按钮 确认、清空等
    table_btn3 = (By.CSS_SELECTOR, 'td[class="button"]')  # 表格下的按钮 确 认、恢 复、取 消等
    table_checkboxs = (By.CSS_SELECTOR, 'div#tableContainer >table >tbody >tr >td >input[type="checkbox"]')  # 表格所有的checkbox
    # 关闭弹窗或者打开弹窗导致不响应的按钮处理
    open_or_close_by = (By.CSS_SELECTOR, 'span[class="btn_box"]') # onclick="doCreation()" onclick="newApply()"  viewTab()

    # 数据详情页编辑table，据观察table都是id=dztabl
    editTable = (By.ID, 'dztable')
    editTrs = (By.CSS_SELECTOR, 'table#dztable >tbody >tr')
    editTds = (By.CSS_SELECTOR, 'table#dztable >tbody >tr >td')
    editTdTags = (By.CSS_SELECTOR, 'table#dztable >tbody >tr >td >[class^=fftd]')

    # 页面左侧菜单
    img_shows = (By.CSS_SELECTOR, 'img.node_icon.gray_arrow') # 按下显示隐藏的菜单
    left_links = (By.CSS_SELECTOR, 'a.pt9song')  # 所有左侧菜单

    # 弹出窗口右上角刷新 关闭按钮
    shuaimg = (By.ID, 'button1')
    closeimg = (By.ID, 'button2')

    # 营销活动输入控件
    market_widget = (By.CSS_SELECTOR, "form#form1 >table >tbody >tr >td.dw_conacte >table >tbody >tr >td")
    market_table_widget = (By.CSS_SELECTOR, "form[name='form1'] >div >table >tbody >tr")
    market_win_widget = (By.CSS_SELECTOR, "form[name='form1'] >div >table >tbody >tr >td >input")
    market_channel = (By.CSS_SELECTOR, "form#form1 >table >tbody >tr >td")
    #产品管理界面控件
    product_management = (By.CSS_SELECTOR, "form#form1 >table >tbody >tr >td")
    product_management_info = (By.CSS_SELECTOR, "form#form1 >table >tbody >tr >td >table >tbody >tr >td")

    # findAlls用法 参数1是表示等待时间秒， 参数2是上面的By元组，表示查询的控件
    # 仅对元素列表有效find_elements，单个元素的识别还未做
    # 例如：seltrs = self.findAlls(6, *(self.selectList1, self.selectList2))
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



    # 进入iframe框架的方法，参数*ifmname为iframe html标签的name，可以输入多个表示进入多层嵌套的iframe中
    def comeinifm(self, *ifmname):
        driver = self.driver
        try:
            driver.set_page_load_timeout(15)
            driver.implicitly_wait(15)
            driver.switch_to_window(driver.current_window_handle)
        except NoSuchWindowException as e:
            self.logstu.debug('comein iframe NoSuchWindowException')
            self.goLastOneWindow()
        except UnexpectedAlertPresentException as e:
            self.logstu.debug('UnexpectedAlertPresentException')
            alttxt = self.close_alert_and_get_its_text()
            self.logstu.debug(alttxt)
        except:
            self.logstu.debug('可能遇到了：raise ResponseNotReady()')
            self.logstu.debug(driver.title)
            self.logstu.debug(driver.current_window_handle)
            self.logstu.debug(driver.window_handles)

        if len(ifmname) == 0:
            return
        for ifm in range(0, len(ifmname)):
            self.logstu.debug('switch to frame :' + ifmname[ifm]
                              + '\n\tBrowser Title:' + driver.title.strip()
                              + '\n\tBrowser window handle:' + driver.current_window_handle)
            try:
                driver.switch_to_frame(driver.find_element_by_name(ifmname[ifm]))
            except NoSuchElementException as e:
                self.logstu.debug(e)

    # 左侧菜单方法用法如下，参数1是菜单格式例如：复审>审核中
    # 第二个之后的参数为左侧菜单所在iframe  ‘初审>审核中’
    # 该方法精确匹配菜单名称
    def leftMenuClick(self, menus_excel, *ifm):
        driver = self.driver
        if menus_excel == '':
            return
        if len(ifm) > 0:
            self.comeinifm(*ifm)
        treeTab = driver.find_element_by_css_selector('table#tabTreeview')
        for caidan3 in range(0, 5):
            leftimgs = treeTab.find_elements(*self.img_shows)
            if len(leftimgs) == 0:
                break
            if len(leftimgs) > 0:
                for img in leftimgs:
                    if img.is_displayed():
                        driver.set_page_load_timeout(10)
                        try:
                            img.click()
                        except TimeoutException as e:
                            self.logstu.debug('leftMenuVagueClick + button click() TimeoutException')
        self.logstu.info(u'左侧菜单操作：' + self.all_type_to_unicode(menus_excel))
        menus_excel = self.all_type_to_encode(menus_excel).split('>')
        menus_excel_value = 0
        for i in range(0, 3):
            try:
                leftmenus = treeTab.find_elements(*self.left_links)
                for menu in leftmenus:
                    if self.all_type_to_encode(menu.text) == menus_excel[menus_excel_value]:
                        menu.click()
                        if self.is_alert_present(self.driver):
                            try:
                                self.driver.switch_to_alert().accept()
                            except NoAlertPresentException as e:
                                self.logstu.debug('leftMenuClick NoAlertPresentException')
                                #self.logstu.debug(e)
                        menus_excel_value = menus_excel_value + 1
                        if menus_excel_value >= len(menus_excel):
                            break
                return
            except StaleElementReferenceException as e:
                self.logstu.debug('leftMenuClick StaleElementReferenceException')
                #self.logstu.debug(e)


    # 左侧菜单方法用法如下，参数1是菜单格式例如：复审>审核中
    # 第二个之后的参数为左侧菜单所在iframe  ‘初审>审核中’
    # 该方法模糊匹配菜单名称，只要第一个找到的菜单包含参数菜单就点击
    def leftMenuVagueClick(self, menus_excel, *ifm):
        driver = self.driver
        if menus_excel == '':
            return
        if len(ifm) > 0:
            self.comeinifm(*ifm)

        treeTab = driver.find_element_by_css_selector('table#tabTreeview')
        for caidan3 in range(0,5):
            leftimgs = treeTab.find_elements(*self.img_shows)
            if len(leftimgs) == 0:
                break
            if len(leftimgs) > 0:
                for img in leftimgs:
                    if img.is_displayed():
                        driver.set_page_load_timeout(10)
                        try:
                            img.click()
                        except TimeoutException as e:
                            self.logstu.debug('leftMenuVagueClick + button click() TimeoutException')
                            #self.logstu.debug(e)

        self.logstu.info(u'左侧菜单操作：' + self.all_type_to_unicode(menus_excel))
        menus_excel = self.all_type_to_encode(menus_excel).split('>')
        menus_excel_value = 0
        for i in range(0, 3):
            try:
                leftmenus = treeTab.find_elements(*self.left_links)
                for menu in leftmenus:
                    if self.all_type_to_encode(menu.text).find(menus_excel[menus_excel_value]) != -1:
                        menu.click()
                        if self.is_alert_present(self.driver):
                            try:
                                self.driver.switch_to_alert().accept()
                            except NoAlertPresentException as e:
                                self.logstu.debug('leftMenuVagueClick NoAlertPresentException')
                        menus_excel_value = menus_excel_value + 1
                        if menus_excel_value >= len(menus_excel):
                            break
                return
            except StaleElementReferenceException as e:
                self.logstu.debug('leftMenuVagueClick StaleElementReferenceException')
                #self.logstu.debug(e)

    # 设置查询条件，先判断查询条件是否展开，
    #  selnum ：int值从1开始，表示要编辑的查询条件列表第几行条件
    #  selectnum ： int值从1开始，表示条件select标签选择第几个 等于 以...开始 等
    #  setvalue ： 查询条件选择后，第一个输入框输入的数据
    def select_set(self, otrnum, oselectnum, *setvalues):
        trnum = int(otrnum)
        selectnum = int(oselectnum)
        driver = self.driver
        #selclass = PubSelectItemElement()

        # 判断查询条件前 + 是否显示，显示表示查询条件被隐藏，点击使其显示出来
        selectjia = driver.find_element(*self.filterIconPlus)
        if selectjia.is_displayed():
            selectjia.click()
            driver.find_element(*self.filterIconMinus)

        # 判断参数是否合法
        #seltrs = driver.find_elements(*self.selectList1)
        seltrs = self.findAlls(6, *(self.selectList1, self.selectList2))
        len_sellist = len(seltrs)
        self.logstu.debug(u'查询条件列表数量：' + str(len_sellist))
        if trnum > len_sellist:
            self.logstu.debug(u'查询选项的行数超过了实际选项数据')
            return
        edittr = seltrs[trnum - 1]
        self.logstu.debug(u'当前编辑的查询条件【' + edittr.find_element_by_tag_name('td').text + u'】')

        # 下拉选择查询条件的范围：等于、 在...之间
        select = edittr.find_element_by_tag_name('select')
        allOptions = select.find_elements_by_tag_name("option")
        allOptions[selectnum -1].click()
        time.sleep(0.5)

        valueconut = 0
        valuelen = len(setvalues)
        tdall = edittr.find_elements_by_css_selector('[name^="DOFILTER"][name$="VALUE"]')
        for td in range(0, len(tdall)):
            if tdall[td].is_displayed() == False:
                continue
            if valueconut >= valuelen:
                break

            if tdall[td].tag_name == 'select':
                allOptions = tdall[td].find_elements_by_tag_name("option")
                for v in allOptions:
                    if self.all_type_to_encode(v.text) == self.all_type_to_encode(setvalues[valueconut]):
                        v.click()
                        valueconut = valueconut + 1
                        break
            if tdall[td].tag_name == 'input':
                tdall[td].clear()
                tdall[td].send_keys(self.all_type_to_unicode(setvalues[valueconut]))
                valueconut = valueconut + 1

    # 设置查询条件，先判断查询条件是否展开，
    #  queryName ：查询条件的名称，例如：商品编码  商户名称 等
    #  queryRange ： 查询范围下拉选择，表示条件select标签选择 等于 以...开始 等
    #  setvalue ： 查询条件选择后，第一个输入框输入的数据
    def selectAutoSet(self, queryName, queryRange, *setvalues):
        queryName = self.all_type_to_encode(queryName)
        queryRange = self.all_type_to_encode(queryRange)
        driver = self.driver
        for i in range(0, 5):
            try:
                # 判断查询条件前 + 是否显示，显示表示查询条件被隐藏，点击使其显示出来
                try:
                    selectjia = driver.find_element(*self.filterIconPlus)
                    if selectjia.is_displayed():
                        selectjia.click()
                        driver.find_element(*self.filterIconMinus)
                except NoSuchElementException as e:
                    self.logstu.debug(e)
                    try:
                        selectjian = driver.find_element(*self.filterIconMinus)
                        self.logstu.debug('查询条件列表已经显示出来了，继续后面的操作')
                    except NoSuchElementException as e:
                        self.logstu.error('查询条件列表的 + 和 - 都没有找到')
                        if i >= 6:
                            self.logstu.error('查询条件列表的 + 和 - 都没有找到')
                        time.sleep(1)
                        continue

                    # 判断参数是否合法
                seltrs = self.findAlls(6, *(self.selectList1, self.selectList2))
                len_sellist = len(seltrs)
                self.logstu.debug('查询条件个数:' + str(len_sellist))
                for seltr in seltrs:
                    self.logstu.debug(u'当前是：' + seltr.find_elements_by_tag_name('td')[0].text +
                                      u' | 目标查询条件：' + self.all_type_to_unicode(queryName))
                    if self.all_type_to_encode(seltr.find_elements_by_tag_name('td')[0].text).strip() == queryName:
                        # 下拉选择查询条件的范围：等于、 在...之间
                        select = seltr.find_elements_by_tag_name('td')[1].find_element_by_tag_name('select')
                        allOptions = select.find_elements_by_tag_name("option")
                        for option in allOptions:
                            if self.all_type_to_encode(option.text).strip() == queryRange:
                                option.click()
                                break
                        valueconut = 0
                        valuelen = len(setvalues)
                        tdall = seltr.find_elements_by_css_selector('[name^="DOFILTER"][name$="VALUE"]')
                        for td in range(0, len(tdall)):
                            if tdall[td].is_displayed() == False:
                                continue
                            if valueconut >= valuelen:
                                break
                            if tdall[td].tag_name == 'select':
                                allOptions = tdall[td].find_elements_by_tag_name("option")
                                for v in allOptions:
                                    if self.all_type_to_encode(v.text) == self.all_type_to_encode(
                                            setvalues[valueconut]):
                                        v.click()
                                        valueconut = valueconut + 1
                                        break
                            if tdall[td].tag_name == 'input':
                                tdall[td].clear()
                                tdall[td].send_keys(self.all_type_to_unicode(setvalues[valueconut]))
                                valueconut = valueconut + 1
                        return
            except StaleElementReferenceException as e:
                self.logstu.debug(u'发生异常 StaleElementReferenceException 重试一次')
                #self.logstu.debug(e)
                continue




    # 用上面单个设置查询条件的方法select_set，实现查询条件列表全部一起输入方法
    def select_sets(self, dict_data):
        for count in range(1, 8):
            strcount = '查询条件' + str(count)
            sel_text = self.all_type_to_encode(dict_data[strcount])
            if sel_text == '':
                continue
                self.logstu.debug(strcount + ':' + sel_text)
            self.select_set(count, *tuple(sel_text.split('|')))

    # 用上面单个设置查询条件的方法selectAutoSet，实现查询条件列表全部一起输入方法
    def selectAutoSets(self, dict_data):
        for count in range(1, 8):
            strcount = '查询条件' + str(count)
            sel_text = self.all_type_to_encode(dict_data[strcount])
            if sel_text == '':
                continue
            self.logstu.debug(strcount + ':' + sel_text)
            self.selectAutoSet(*tuple(sel_text.split('|')))
        time.sleep(1)
        self.select_btn(u'查询')

    # 同selectAutoSet，参数为 商户名称-等于-kfc,商户编码-包含-pd222  格式的字符串
    def selectAutoSets2(self, select_data):
        sels = self.all_type_to_encode(select_data).split(',')
        for sel in sels:
            self.selectAutoSet(*tuple(sel.split('-')))
        self.select_btn(u'查询')

    # 输入查询条件，并按下查询按钮
    def selectSetAndBtn(self, dict_data):
        self.select_sets(dict_data)
        self.select_btn(u'查询')


    # 查询条件下的按钮，如：查询  清空  恢复  取消
    def select_btn(self, btn_name1):
        driver = self.driver
        btn_name = self.all_type_to_encode(btn_name1)
        selectjia = driver.find_element(*self.filterIconPlus)
        if selectjia.is_displayed():
            selectjia.click()
            time.sleep(0.5)
        btns = driver.find_elements(*self.selectTabBtn)
        self.logstu.debug(u'btns:' + str(len(btns)) + u'| 目标btnname：' + self.all_type_to_unicode(btn_name))
        for btn in range(0, len(btns)):
            self.logstu.debug(u'number ' + str(btn) + u' btn text is:' + btns[btn].get_attribute('value'))
            if btns[btn].get_attribute('value').encode('utf8') == btn_name:
                btns[btn].click()
                return
        raise Exception(u'没有找到按钮 ' + self.all_type_to_unicode(btn_name.__str__()))

    # 获取表格数据行数
    def table_getRowsCount(self):
        driver = self.driver
        #tabclass = PubTableItemElement()
        #driver = webdriver.Firefox()
        table_tr = driver.find_elements(*self.table_tr)
        return len(table_tr) - 2 # 去掉标题行及一个隐藏行

    # 判断查询出来的数据是否有一条以上  如果没有,写到执行结果里
    def is_table_getRowsCount_exist(self,row,comm):
        count = self.table_getRowsCount()
        if count > 0:
            return count
        else:
            self.logstu.info("查询不到对应的数据")
            return -1

    # 点击标题排序，参数
    # cname 表示列名，即排序的列标题
    # sort_state 取值 zx 表示正序  fx 反序
    def table_get_th(self, cname):
        cname = self.all_type_to_encode(cname)
        table_ths = self.findAlls(6, *(self.table_th, self.table_th2))
        if len(table_ths) == 0:
            raise Exception(u'未找到表格的th')
        for th in table_ths:
            self.logstu.debug('%s | %s' % (self.all_type_to_encode(th.text), cname))
            if self.all_type_to_encode(th.text).find(cname) != -1:
                #self.logstu.debug('break')
                return th
        raise Exception(u'未找到表格的%s列' %(cname.__str__()))
    def table_th_sort(self, cname, sort_state):
        element_th = self.table_get_th(cname)
        img = ''
        try:
            img = element_th.find_element_by_tag_name('img')
        except NoSuchElementException as e:
            self.logstu.debug('<img> NoSuchElementException')
        if sort_state == 'zx':
            if img == '':
                return
            elif img.get_attribute('class') == 'sort_up':
                return
            else:
                element_th.click()
                for i in range(0, 10):
                    time.sleep(1)
                    try:
                        img = element_th.find_element_by_tag_name('img')
                        if img.get_attribute('class') == 'sort_up':
                            return
                    except StaleElementReferenceException as e:
                        self.logstu.debug('StaleElementReferenceException')
                    except NoSuchElementException as e:
                        self.logstu.debug('<img> click NoSuchElementException')
                    except WebDriverException as e:
                        self.logstu.debug(e)
                        element_th = self.table_get_th(cname)
        if sort_state == 'fx':
            if img == '':
                element_th.click()
            elif img.get_attribute('class') == 'sort_up':
                element_th.click()
            else:
                return
            for i in range(0,10):
                time.sleep(1)
                try:
                    img = element_th.find_element_by_tag_name('img')
                    if img.get_attribute('class') == 'sort_down':
                        return
                except StaleElementReferenceException as e:
                    self.logstu.debug('StaleElementReferenceException')
                except NoSuchElementException as e:
                    self.logstu.debug('<img> click NoSuchElementException')
                except WebDriverException as e:
                    self.logstu.debug(e)
                    element_th = self.table_get_th(cname)



    # 获取表格数据列数
    def table_getColumnsCount(self):
        driver = self.driver
        #table_th = driver.find_elements(*self.table_th)
        table_th = self.findAlls(6, *(self.table_th, self.table_th2))
        return len(table_th) - 1 # 去掉序号列

    # 获取指定行和列的单元格数据，参数为：
    #   rownum ：指定的行数，不包含标题行，从1开始
    #   colnum ：指定的的列数，不包含序号列，从1开始
    def table_getValue(self, rownum, colnum):
        driver = self.driver
        #tabclass = PubTableItemElement()
        trownum = self.table_getRowsCount()
        tcolnum = self.table_getColumnsCount()
        if rownum > trownum :
            self.logstu.info(u'搜索的行数 '+ str(rownum) + u' 超过了实际表格行数' + str(trownum))
            return "NULL"
        if colnum > tcolnum:
            self.logstu.info(u'搜索的列数 ' + str(colnum) + u' 超过了实际表格列数' + str(tcolnum))
            return "NULL"
        table_tr = driver.find_elements(*self.table_tr)[rownum + 1] # 排除标题和隐藏行，参数rownum + 1就是需要的行标
        table_td = table_tr.find_elements_by_tag_name('td')[colnum]    # 第0列是序号列，数据列从1开始
        table_td_input = table_td.find_element_by_tag_name('input').get_attribute('value')
        return self.all_type_to_encode(table_td_input)

    # 获取指定行和列的单元格数据，参数为：
    #   rownum ：指定的行数，不包含标题行，从1开始
    #   colnum ：指定的的列数，不包含序号列，从1开始
    #   values ：表单中要输入的值
    #add by zhuoshenghua
    def table_setValue(self, rownum, colnum,values):
        driver = self.driver
        #tabclass = PubTableItemElement()
        trownum = self.table_getRowsCount()
        tcolnum = self.table_getColumnsCount()
        value = values
        if rownum > trownum :
            self.logstu.info(u'搜索的行数 '+ str(rownum) + u' 超过了实际表格行数' + str(trownum))
            return "NULL"
        if colnum > tcolnum:
            self.logstu.info(u'搜索的列数 ' + str(colnum) + u' 超过了实际表格列数' + str(tcolnum))
            return "NULL"
        table_tr = driver.find_elements(*self.table_tr)[rownum + 1] # 排除标题和隐藏行，参数rownum + 1就是需要的行标
        table_td = table_tr.find_elements_by_tag_name('td')[colnum]    # 第0列是序号列，数据列从1开始
        table_td.find_element_by_tag_name('input').send_keys(self.all_type_to_encode(value))

    # 根据标题名称查找所在列数
    def table_getColnum(self, colnumName1):
        driver = self.driver
        colnumName = self.all_type_to_encode(colnumName1)
        #tabclass = PubTableItemElement()
        itable = driver.find_element(*self.xntable)
        table_ths = itable.find_elements_by_tag_name('th')
        for i in range(0, len(table_ths)):
            self.logstu.debug('查询列：'+ self.all_type_to_encode(table_ths[i].text).strip() + ' | ' + colnumName)
            if self.all_type_to_encode(table_ths[i].text).strip() == colnumName:
                self.logstu.debug(self.all_type_to_unicode(colnumName) + u' 对应列数为：' + str(i))
                return i
        self.logstu.info(u'未找到列: ' + self.all_type_to_unicode(colnumName))
        return -1

    # 根据列标题和行数查询表格数据
    def table_getValue2(self, rownum, colnumName1):
        colnumName = self.all_type_to_encode(colnumName1)
        try:
            colnum = self.table_getColnum(colnumName)
        except Exception as e:
            self.logstu.debug(e)
            colnum = -1
            #self.table_getValue2(rownum, colnumName1)
        if colnum != -1:
            return self.table_getValue(rownum, colnum)
        return '未找到 ' + str(rownum) + ' 行 ' + colnumName + ' 列的数据'

    # 选择行数
    def table_RowClick(self, rownum):
        driver = self.driver
        #tabclass = PubTableItemElement()
        #driver.find_elements(*self.table_tr)[rownum + 1].click()
        num = self.table_getColumnsCount()
        for i in range(0,10):
            rown = len(driver.find_elements(*self.table_tr))
            self.logstu.debug('当前表格行数 %d' % (rown))
            if rown > 0:
                break
            time.sleep(1)
        if rown - 1 < rownum + 1:
            raise Exception('Not found %d Row Data，no select this row。' % (rownum))
        if num >= 3:
            try:
                driver.find_elements(*self.table_tr)[rownum + 1].find_elements_by_tag_name('td')[2].click()
            except IndexError as e:
                self.logstu.debug(e)
                time.sleep(0.5)
                driver.find_elements(*self.table_tr)[rownum + 1].find_elements_by_tag_name('td')[num - 1].click()
        else:
            driver.find_elements(*self.table_tr)[rownum + 1].find_elements_by_tag_name('td')[num-1].click()

    # 点选表格某一行的checkbox
    def table_RowCheckBox(self, rownum):
        driver = self.driver
        tr = driver.find_elements(*self.table_tr)[rownum + 1]
        checkbox = tr.find_element_by_css_selector('input[type="checkbox"]')
        self.logstu.debug(u'checkbox click before checked state (is √):' + checkbox.get_attribute('value'))
        checkbox.click()
        self.logstu.debug(u'checkbox click after checked state (is √):' + checkbox.get_attribute('value'))

    # 表格的操作按钮：新增 详情  等
    def table_BtnClick(self, btnname1):
        driver = self.driver
        olds = driver.window_handles
        self.timeoutBtnClick(btnname1)
        news = driver.window_handles
        self.logstu.debug(self.is_alert_and_close_and_get_text())
        if len(news) == len(olds):
            self.logstu.debug(u'按钮按下后没有打开或者关闭窗口')
        elif len(news) > len(olds):
            self.goNewWindow(olds)
        elif len(news) < len(olds):
            self.goLastOneWindow()
        elif self.is_alert_present2():
            try:
                self.logstu.info(self.driver.switch_to_alert().text)
            except NoAlertPresentException as e:
                #self.logstu.debug(e)
                self.logstu.debug('table_BtnClick 判断是否有弹窗时发生： NoAlertPresentException')
            except NoSuchWindowException as e:
                self.logstu.debug('table_BtnClick 判断是否有弹窗时发生：NoSuchWindowException')
                self.goLastOneWindow()

    # 表格的操作按钮：新增 详情  等
    def table_BtnClick_no_close_alert(self, btnname1):
        driver = self.driver
        olds = driver.window_handles
        self.timeoutBtnClick(btnname1)
        news = driver.window_handles
        #self.logstu.debug(self.is_alert_and_close_and_get_text())
        if len(news) == len(olds):
            self.logstu.debug(u'按钮按下后没有打开或者关闭窗口')
        elif len(news) > len(olds):
            self.goNewWindow(olds)
        elif len(news) < len(olds):
            self.goLastOneWindow()
        elif self.is_alert_present2():
            try:
                self.logstu.info(self.driver.switch_to_alert().text)
            except NoAlertPresentException as e:
                #self.logstu.debug(e)
                self.logstu.debug('table_BtnClick 判断是否有弹窗时发生： NoAlertPresentException')
            except NoSuchWindowException as e:
                self.logstu.debug('table_BtnClick 判断是否有弹窗时发生：NoSuchWindowException')
                self.goLastOneWindow()

    def timeoutBtnClick(self, btnname1):
        driver = self.driver
        btnname = self.all_type_to_encode(btnname1)
        # tabclass = PubTableItemElement()
        btns = driver.find_elements(*self.table_btn)
        if len(btns) == 0:
            self.logstu.info(u'未找到按钮(没有定位到任何按钮)：' + self.all_type_to_unicode(btnname))
            return False
        for btn in range(0, len(btns)):
            findname = btns[btn].text
            self.logstu.debug(u'button for:' + str(btn) + u' | button name:' + findname)
            if self.all_type_to_encode(findname) == btnname:
                try:
                    driver.set_page_load_timeout(1)
                    btns[btn].click()
                    return True
                except TimeoutException as e:
                    self.logstu.info(e)
                    driver.set_page_load_timeout(15)
                    return True
                except Exception as e:
                    self.logstu.info(e)
                    driver.set_page_load_timeout(15)
                    return True
                    #self.logstu.info(e)
        raise Exception(u'未找到按钮（没有找到指定名字的按钮）： ' + self.all_type_to_unicode(btnname.__str__()))

    def thread_mothed(self):
        try:
            self.timeoutBtnClick(self.tmp)
        except:
            self.logstu.info(u'button click except')

    def base_thread_btn(self, btnname1):
        self.tmp = btnname1
        driver = self.driver
        olds = driver.window_handles
        try:
            ttt = threading.Thread(target=self.thread_mothed)
            self.logstu.debug(u'thread_btn new window thread start!')
            ttt.start()
            ttt.join(1)
        except Exception as e:
            self.logstu.debug(u'thread fail!')

    def thread_btn(self, btnname1):
        self.tmp = btnname1
        driver = self.driver
        olds = driver.window_handles
        try:
            ttt = threading.Thread(target=self.thread_mothed)
            self.logstu.debug(u'thread_btn new window thread start!')
            ttt.start()
            ttt.join(1)
        except Exception as e:
            self.logstu.debug(u'thread fail!')
        finally:
            for i in range(0, 10):
                try:
                    news = self.driver.window_handles
                    break
                except Exception as e:
                    self.logstu.debug('raise CannotSendRequest() => ' + str(i))
                    time.sleep(1)
            self.logstu.debug(news)
            self.logstu.debug(olds)
            if len(news) == len(olds):
                self.logstu.debug(u'按钮按下后没有打开或者关闭窗口')
            elif len(news) > len(olds):
                self.logstu.debug(u'按钮按下后发现新窗口')
                self.goNewWindow(olds)
            elif len(news) < len(olds):
                self.logstu.debug(u'按钮按下后关闭了当前窗口')
                self.goLastOneWindow()

    # 多线程打开窗口
    def thread_mothed2(self):
        try:
            self.element.click()
        except Exception as e:
            self.logstu.info(u'button click except')

    # 多线程打开窗口，参数是selenium 控件类型
    def thread_btn2(self, element):
        self.element = element
        driver = self.driver
        olds = driver.window_handles
        try:
            ttt = threading.Thread(target=self.thread_mothed2)
            self.logstu.debug(u'thread_btn2 new window thread start!')
            ttt.start()
            ttt.join(1)
        except Exception as e:
            self.logstu.debug(u'thread fail!')
        finally:
            for i in range(0,10):
                try:
                    news = self.driver.window_handles
                    break
                except:
                    self.logstu.debug('raise CannotSendRequest() => ' + str(i))
                    time.sleep(1)
            self.logstu.debug(news)
            self.logstu.debug(olds)
            if self.is_alert_present2() == True:
                return
            if len(news) == len(olds):
                self.logstu.debug(u'按钮按下后没有打开或者关闭窗口')
            elif len(news) > len(olds):
                self.logstu.debug(u'按钮按下后发现新窗口')
                self.goNewWindow(olds)
            elif len(news) < len(olds):
                self.logstu.debug(u'按钮按下后关闭了当前窗口')
                self.goLastOneWindow()


    def table_BtnClick_NoSetTimeOut(self, btnname1):
        driver = self.driver
        btnname = self.all_type_to_encode(btnname1)
        # tabclass = PubTableItemElement()
        btns = driver.find_elements(*self.table_btn)
        if len(btns) == 0:
            self.logstu.info(u'未找到按钮(没有定位到任何按钮)：' + self.all_type_to_unicode(btnname))
            return False
        for btn in range(0, len(btns)):
            findname = btns[btn].text
            self.logstu.debug(u'button for:' + str(btn) + u' | button name:' + findname)
            if self.all_type_to_encode(findname) == btnname:
                # webdriver.Firefox().set_script_timeout(1)
                try:
                    self.logstu.debug(u'set_page_load_timeout 1')
                    driver.set_page_load_timeout(15)
                    btns[btn].click()
                except TimeoutException as e:
                    #self.logstu.info(e)
                    self.logstu.info('table_BtnClick_NoSetTimeOut 按钮按下后： TimeoutException')
                    time.sleep(1)
                    self.goLastOneWindow()
                if self.is_alert_present(self.driver):
                    try:
                        self.logstu.info(self.driver.switch_to_alert().text)
                    except NoAlertPresentException as e:
                        self.logstu.debug(findname + ' click after not found AlertWindow.')
                    except NoSuchWindowException as e:
                        self.logstu.debug('table_BtnClick_NoSetTimeOut NoSuchWindowException')
                        self.goLastOneWindow()
                return True
        raise Exception(u'未找到按钮（没有找到指定名字的按钮）： ' + self.all_type_to_unicode(btnname.__str__()))

    # 表格的操作按钮：新增 详情  等
    def open_or_close_BtnClick(self, btnname1):
        driver = self.driver
        btnname = self.all_type_to_encode(btnname1)
        # tabclass = PubTableItemElement()
        btns = driver.find_elements(*self.open_or_close_by)
        if len(btns) == 0:
            self.logstu.info(u'未找到按钮(没有定位到任何按钮)：' + self.all_type_to_unicode(btnname))
            return False
        for btn in range(0, len(btns)):
            #webdriver.Firefox.find_element_by_css_selector().get_attribute()
            findname = btns[btn].get_attribute('title')

            self.logstu.debug(u'button for:' + str(btn) + u' | button name:' + findname)
            if self.all_type_to_encode(findname) == btnname:
                olds = driver.window_handles
                findonclick = btns[btn].get_attribute('onclick')
                js = 'window.' + findonclick
                self.logstu.debug(js)
                driver.set_script_timeout(1)
                #driver.execute_script(js)
                driver.execute_async_script(js)
                self.logstu.debug('js execute end!')
                for lenwin in range(0,10):
                    news = driver.window_handles
                    if len(olds) != len(news):
                        break
                    time.sleep(0.5)
                self.goLastOneWindow()
                if self.is_alert_present(self.driver):
                    try:
                        self.logstu.info(findname + u' click after alert window')
                    except NoAlertPresentException as e:
                        self.logstu.debug(findname + u' click after not found AlertWindow.')
                return True
        raise Exception(u'未找到按钮（没有找到指定名字的按钮）： ' + self.all_type_to_unicode(btnname.__str__()))

    # 弹出选择则框确认按钮， input按钮文字在value属性显示
    def table_BtnClick2(self, btnname1):
        driver = self.driver
        btnname = self.all_type_to_encode(btnname1)
        # tabclass = PubTableItemElement()
        btns = driver.find_elements(*self.table_btn2)
        if len(btns) == 0:
            raise Exception('未找到按钮(没有定位到任何按钮)：' + btnname)
        for btn in range(0, len(btns)):
            findname = btns[btn].get_attribute('value')
            self.logstu.debug(u'for select button ' + str(btn) + u' : ' + findname
                              + u' --> 目标button：' + self.all_type_to_unicode(btnname))
            if self.all_type_to_encode(findname) == btnname:
                btns[btn].click()
                return True
        raise Exception('未找到按钮（没有找到指定名字的按钮）：' + btnname)

    # 弹出页面确 定、恢 复、取 消按钮， td按钮文字在text属性显示
    #Add by zhuoshenghua
    def table_BtnClick3(self, btnname1):
        driver = self.driver
        btnname = self.all_type_to_encode(btnname1).strip()
        btns = driver.find_elements(*self.table_btn3)
        if len(btns) == 0:
            raise Exception('未找到按钮(没有定位到任何按钮)：' + btnname)
        for btn in range(0, len(btns)):
            findname = btns[btn].text.strip()
            self.logstu.debug(u'for select button ' + str(btn) + u' : ' + findname
                              + u' --> 目标button：' + self.all_type_to_unicode(btnname))
            if self.all_type_to_encode(findname) == btnname:
                btns[btn].click()
                return True
        raise Exception('未找到按钮（没有找到指定名字的按钮）：' + btnname)
		
	#点击按钮操作，add by limeng
    def click_btn(self, element):
        try:
            element.click()
        except Exception as e:
            self.logstu.info(u'button click except：')
            self.logstu.info(e)

    #输入框输入内容，add by limeng
    def input_text(self,element,text):
        try:
            element.click()
            element.clear()
            element.send_keys(text)
            self.logstu.info(u'输入框填写为：%s' %text )
        except Exception as e:
            self.logstu.info(u'input text except：')
            self.logstu.info(e)
    #多选框选择对应内容，add by limeng
    def option(self,select_btn,value):
        list = select_btn.find_elements_by_xpath("//option[@value]" )# 选择拒绝的原因
        #选择拒绝原因
        #self.logstu.info("value is %s type is %s"  % (value,type(value)))
        for btn in list:
            if btn.text == value:
                self.logstu.info(u"选择下拉框中的：%s" % value)
                btn.click()
                return
        raise Exception(u'没有找到下拉框中的值：' + self.all_type_to_unicode(value.__str__()))
    #点击对应的title add by limeng
    def click_text_btn(self, text_name,type):
        #确定按钮属性
        type_dit = {"title":self.title_btn}
        element = type_dit[type]

        driver = self.driver
        title_name = self.all_type_to_encode(text_name)
        btns = driver.find_elements(*element)
        if len(btns) == 0:
            self.logstu.info(u'未找到按钮(没有定位到任何按钮)：' + self.all_type_to_unicode(text_name))
            return False
        for btn in range(0, len(btns)):
            findname = btns[btn].text
            self.logstu.debug(u'button for:' + str(btn) + u' | button name:' + findname)
            if self.all_type_to_encode(findname) == title_name:
                try:
                    driver.set_page_load_timeout(1)
                    btns[btn].click()
                    return True
                except TimeoutException as e:
                    self.logstu.info(e)
                    driver.set_page_load_timeout(15)
                    return True
                except Exception as e:
                    self.logstu.info(e)
                    driver.set_page_load_timeout(15)
                    return True
                    #self.logstu.info(e)
        raise Exception(u'未找到按钮（没有找到指定按钮）： ' + self.all_type_to_unicode(title_name.__str__()))
    #根据输入数据选择表格中的对应行数据
    def table_text_clicks(self,dict_data):
        for count in range(1, 41):
            strcount = '输入值' + str(count)
            if dict_data[strcount] == '':
                continue
            sel_text = dict_data[strcount]

            #self.logstu.debug(self.all_type_to_unicode(strcount) + u'|' + self.all_type_to_unicode(sel_text))
            if len(sel_text.split('|')) == 1:
                self.logstu.debug(self.all_type_to_unicode(strcount) + u'|' + self.all_type_to_unicode(sel_text))
                self.table_text_click(sel_text)
    #根据文本选择表格中的某行数据  add by limeng
    def table_text_click(self,text_name):
        driver = self.driver
        tds = driver.find_elements(*self.table_td)
        self.logstu.debug(u"选择表格中的 %s 这一行" %text_name)
        flag = 0
        for i in range(len(tds)):
            try:
                s = tds[i].find_element_by_tag_name("input")
            except Exception as e:
                continue
            if s.get_attribute("value") == text_name:
                tds[i].click()
                flag = 1
                break
        if flag == 0:raise Exception(u'表格中未找到指定值： ' + self.all_type_to_unicode(text_name.__str__()))
        id = tds[i].get_attribute("id")
        num = int(id.split('F')[1])
        #如果有checkbox，点击checkbox
        if tds[i-num+1].find_element_by_tag_name("input").get_attribute("type") == "checkbox":
            tds[i - num + 1].click()
    # 输入条件    add by limeng
    #dice_data 是数据 ，menu是确定对应的页面控件 ，ifrm 是对应的iframe
    def input_values(self, dict_data,menu, *ifm):
        if len(ifm) > 0:
            self.comeinifm(*ifm)
        for count in range(1, 41):
            strcount = '输入值' + str(count)
            if dict_data[strcount] == '':
                continue
            sel_text = dict_data[strcount]

            self.logstu.debug(self.all_type_to_unicode(strcount) + u'|' + self.all_type_to_unicode(sel_text))
            if len(sel_text.split('|')) == 2:
                self.input_value(sel_text.split('|')[0], sel_text.split('|')[1],menu ,*ifm)
    # 下拉框和输入框，所有输入条件  market_widget  add by limeng
    def input_value(self,name, value,menu, *ifm):
        if menu == "channel":
            td = self.market_channel
        elif menu == "strategy":
            td = self.market_widget
        elif menu == "product":
            td = self.product_management
        elif menu == "product_info":
            td = self.product_management_info
        driver = self.driver
        name = self.all_type_to_encode(name)
        value = self.all_type_to_encode(value)
        for j in range(0, 10):
            try:
                tds = driver.find_elements(*td)
                break
            except UnexpectedAlertPresentException as e:
                self.logstu.debug(e)
                time.sleep(0.5)

        for i in range(0,len(tds)):
            #self.logstu.info("11111111 "+tds[i].get_attribute('id') +" 22222222222 " +tds[i].__str__())
            if name in self.all_type_to_encode(tds[i].text):
                self.logstu.debug(u"输入控件名称：%s  输入值：%s" % (name, value))
                editinput = tds[i + 1].find_element_by_css_selector('[class^=fftd]')
                #检查扩展选择按钮
                try:
                    inputdate = tds[i + 1].find_element_by_css_selector('input[class="inputdate"][value="..."]')
                except NoSuchElementException as e:
                    inputdate = None
                    #self.logstu.debug(e)
                    pass
                if ( editinput.tag_name == 'textarea' and editinput.get_attribute('readonly') == 'true')  or inputdate != None:
                    selinput = tds[i + 1].find_element_by_css_selector('input[class="inputdate"][value="..."]')
                    driver.set_page_load_timeout(2)
                    self.thread_btn2(selinput)
                    self.comeinifm('ObjectList', 'myiframe0')
                    hands1 = driver.window_handles
                    #oldcurrent = driver.current_window_handle
                    elements = driver.find_elements(*self.market_win_widget)
                    #self.logstu.debug(elements.__str__())
                    value_list = value.split(",")
                    flag = 0
                    for k in range(len(elements)):
                        #self.logstu.debug(elements[k].get_attribute("value"))
                        for m in range(len(value_list)):
                            #self.logstu.debug("11111111111"+value_list[m])
                            if elements[k].get_attribute("value") == value_list[m]:
                                self.logstu.debug(u"%s 中点击：%s" % (name,value_list[m]) )
                                elements[k].click()
                                #新增产品中要点击复选框
                                type = elements[k-1].get_attribute("type")
                                if type == "checkbox":
                                    elements[k-1].click()
                                flag = 1
                                break
                    if flag == 0:raise Exception(u"%s 中没有该按钮 %s" %(name,value))
                    driver.switch_to_default_content()
                    try:
                        ttt = threading.Thread(target=self.table_BtnClick2(u'确认'))
                        self.logstu.debug(u'thread_btn new window thread start!')
                        ttt.start()
                        ttt.join(1)
                        # self.table_BtnClick2(u'确认')
                        hands2 = driver.window_handles
                        #self.logstu.info(hands2.__str__()+hands1.__str__())
                        for t in range(0,10):
                            if len(hands2) < len(hands1):
                                try:
                                    driver.switch_to_window(hands2[-1])
                                except Exception as e:
                                    self.logstu.debug(e)
                    except:
                        self.comeinifm('ObjectList')
                        ttt = threading.Thread(target=self.timeoutBtnClick(u'确定'))
                        self.logstu.debug(u'thread_btn new window thread start!')
                        ttt.start()
                        self.logstu.debug(self.close_alert_and_get_its_text())
                        ttt.join(1)
                        # self.table_BtnClick2(u'确认')
                        hands2 = driver.window_handles
                        self.logstu.info(hands2.__str__() + hands1.__str__())
                        for t in range(0, 10):
                            if len(hands2) < len(hands1):
                                try:
                                    driver.switch_to_window(hands2[-1])
                                except Exception as e:
                                    self.logstu.debug(e)
                    if len(ifm) > 0:
                        self.comeinifm(*ifm)
                    break
                if ( editinput.tag_name == 'input' or editinput.tag_name == 'textarea' ) and editinput.get_attribute('readonly') == None:
                    editinput.clear()
                    editinput.send_keys(self.all_type_to_unicode(value))
                    break
                if editinput.tag_name == 'select':
                    allOptions = editinput.find_elements_by_tag_name("option")
                    for j in range(len(allOptions)):
                        if self.all_type_to_encode(allOptions[j].text) == self.all_type_to_encode(value):
                            allOptions[j].click()
                            break
                    break
                if editinput.tag_name == 'input' and editinput.get_attribute('readonly') == 'true':
                    if name.find('日期') != -1 or name.find('时间') != -1 or u'日' in name:
                        timeinputid = editinput.get_attribute('id')
                        self.logstu.debug(u'日期 or 时间 输入控件 input id = ' + timeinputid)
                        js = 'document.getElementById("'+ timeinputid + '").readOnly =false;'
                        driver.execute_script(js)
                        editinput.clear()
                        editinput.send_keys(self.all_type_to_unicode(value))
                        break
    # 根据文本选择营销活动定义表格中的某一行  add by limeng
    def click_line_and_return_status(self, dict_data):
        driver = self.driver
        for count in range(1, 8):
            strcount = '查询条件' + str(count)
            sel_text = self.all_type_to_encode(dict_data[strcount])
            if sel_text == '':
                continue
            self.logstu.debug(strcount + ':' + sel_text)
            value = sel_text.split("|")[1]
            act = sel_text.split("|")[0]

            for z in range(0, 10):
                try:
                    trs = driver.find_elements(*self.market_table_widget)
                    break
                except UnexpectedAlertPresentException as e:
                    self.logstu.debug(e)
                    time.sleep(0.5)

            for i in range(len(trs)):
                tds = trs[i].find_elements_by_css_selector("td >input")
                for j in range(len(tds)):
                    if tds[j].get_attribute("value") == value:
                        self.logstu.debug(u"点击：%s" % value)
                        try:
                            tds[j].click()
                        except Exception as e:
                            self.logstu.debug(e)

    # 判断字符串是否有unicode，如果有解码为utf8格式
    def all_type_to_encode(self, value):
        if isinstance(value, unicode):
            return value.encode('utf8')
        else:
            return value

    # 判断字符串是否有unicode，如果有解码为utf8格式
    def all_type_to_encode(self, value):
        if isinstance(value, unicode):
            return value.encode('utf8')
        else:
            return value
    # send_keys发送汉字要 unicode格式，这里统一修改
    def all_type_to_unicode(self, str_in):
        # 处理字符编码问题
        if isinstance(str_in, float):
            str_in = int(str_in)
        elif isinstance(str_in, unicode):
            pass
        else:
            str_in = unicode(str_in, "utf-8")
        return str_in

    # 设置表格里面的值，参数为key和value，输入内容的名称找到就自动将value输入其后的td表格的控件中
    # 增加了个参数ifm，标识当前控件在哪一层ifmrame中，操作弹出框选择后会返回到顶层，需要该参数重新回来
    def setEditTableValue(self, tdname1, tdvalue, *ifm):
        driver = self.driver
        tdname = self.all_type_to_encode(tdname1)
        for j in range(0, 10):
            try:
                tds = driver.find_elements(*self.editTds)
                break
            except UnexpectedAlertPresentException as e:
                self.logstu.debug(e)
                time.sleep(0.5)
        self.is_alert_and_close_and_get_text()

        for i in range(0, len(tds)):
            if self.all_type_to_encode(tds[i].text).strip().strip('*').strip() == self.all_type_to_encode(tdname):
                # radios set
                try:
                    driver.implicitly_wait(0.5)
                    iradios = tds[i + 1].find_elements_by_css_selector('input[type="radio"]')
                    if len(iradios) > 0:
                        if tdvalue.split('+') > 1:
                            for rad_i in tdvalue.split('+'):
                                if int(rad_i) <= len(iradios):
                                    iradios[int(rad_i)-1].click()
                        else:
                            iradios[int(tdvalue)-1].click()
                        break
                    driver.implicitly_wait(6)
                except NoSuchElementException as e:
                    driver.implicitly_wait(6)

                # checkbos set
                try:
                    driver.implicitly_wait(0.5)
                    icheckbos = tds[i + 1].find_elements_by_css_selector('input[type="checkbox"]')
                    if len(icheckbos) > 0:
                        if tdvalue.split('+') > 1:
                            for rad_i in tdvalue.split('+'):
                                if int(rad_i) <= len(icheckbos):
                                    icheckbos[int(rad_i) - 1].click()
                        else:
                            icheckbos[int(tdvalue) - 1].click()
                        break
                    driver.implicitly_wait(6)
                except NoSuchElementException as e:
                    driver.implicitly_wait(6)

                editinput = tds[i + 1].find_element_by_css_selector('[class^=fftd]')
                if editinput.tag_name == 'input' and editinput.get_attribute('readonly') == None:
                    editinput.clear()
                    editinput.send_keys(self.all_type_to_unicode(tdvalue))
                    break
                if editinput.tag_name == 'select':
                    allOptions = editinput.find_elements_by_tag_name("option")
                    for v in allOptions:
                        if self.all_type_to_encode(v.text) == self.all_type_to_encode(tdvalue):
                            v.click()
                            break
                    break
                if editinput.tag_name == 'input' and editinput.get_attribute('readonly') == 'true':
                    if tdname.find('日期') != -1 or tdname.find('时间') != -1:
                        timeinputid = editinput.get_attribute('id')
                        self.logstu.debug(u'日期 or 时间 输入控件 input id = ' + timeinputid)
                        js = 'document.getElementById("'+ timeinputid + '").readOnly =false;'
                        driver.execute_script(js)
                        editinput.clear()
                        editinput.send_keys(self.all_type_to_unicode(tdvalue))
                        break
                    selinput = tds[i + 1].find_element_by_css_selector('input[type="button"]')  # [class="inputdate"][value="..."]
                    driver.set_page_load_timeout(1)
                    oldhanlds = driver.window_handles
                    oldcurrent = driver.current_window_handle
                    try:
                        selinput.click()
                        if self.is_alert_present(self.driver):
                            try:
                                alerttext = self.close_alert_and_get_its_text()
                                #self.driver.switch_to_alert().accept()
                                self.logstu.debug(u'按下按钮后弹出了对话框，内容为：\n\t' + alerttext)
                            except NoAlertPresentException as e:
                                self.logstu.debug(u'按下按钮后没有弹出对话框')
                    except TimeoutException as e:
                        self.logstu.debug(e)
                    self.goNewWindow(oldhanlds)

                    # 所属机构 选择使用的是 左侧菜单的方式，不是一般的表格式，需要特殊处理
                    if tdname == '所属机构':
                        self.leftMenuClick(tdvalue,'ObjectList','left')
                        driver.switch_to_window(driver.current_window_handle)
                        self.table_BtnClick2(u'确认')
                        driver.switch_to_window(oldcurrent)
                        if len(ifm) > 0:
                            self.comeinifm(*ifm)
                        break

                    # 判断是否需要使用查询条件
                    if self.all_type_to_encode(tdvalue).find('[') != -1:
                        searchObj = self.all_type_to_encode(tdvalue).split('[')[1]
                        tdvalue = self.all_type_to_encode(tdvalue).split('[')[0]
                        self.comeinifm('ObjectList')
                        self.logstu.debug(u"在弹出的选择窗口中使用查询条件: " + self.all_type_to_unicode(searchObj))
                        self.selectAutoSets2(searchObj)
                    self.comeinifm('ObjectList','myiframe0')
                    self.table_RowClick(int(tdvalue))
                    newtitle = driver.title.strip()
                    self.logstu.debug(u'当前选择窗口的title为：' + newtitle)
                    if self.all_type_to_encode(newtitle) == '请选择所需信息':
                        driver.switch_to_window(driver.current_window_handle)
                        self.table_BtnClick2(u'确认')
                    else:
                        driver.switch_to_default_content()
                        self.comeinifm('ObjectList')
                        self.thread_btn(u'确认')
                        #self.table_BtnClick(u'确认')
                    driver.switch_to_window(oldcurrent)
                    self.logstu.debug(u'当前窗体的title为：' + driver.title)
                    if len(ifm) > 0:
                        self.comeinifm(*ifm)
                    break
                if editinput.tag_name == 'textarea' and editinput.get_attribute('readonly') == None:
                    editinput.clear()
                    editinput.send_keys(self.all_type_to_unicode(tdvalue))
                    break
                if editinput.tag_name == 'textarea' and editinput.get_attribute('readonly') == 'true':
                    selinput = tds[i + 1].find_element_by_css_selector('input[class="inputdate"][value="..."]')
                    driver.set_page_load_timeout(2)
                    oldhanlds = driver.window_handles
                    oldcurrent = driver.current_window_handle
                    try:
                        selinput.click()
                    except TimeoutException as e:
                        self.logstu.debug(e)
                    self.goNewWindow(oldhanlds)
                    self.comeinifm('ObjectList', 'myiframe0')
                    checks = driver.find_elements(*self.table_checkboxs)
                    for num in tdvalue.split('+'):
                        checks[int(num) - 1].click()
                    driver.switch_to_window(driver.current_window_handle)
                    self.table_BtnClick2(u'确认')
                    driver.switch_to_window(oldcurrent)
                    if len(ifm) > 0:
                        self.comeinifm(*ifm)
                    break

    def setEditTableValueFast(self, dict_data, *ifm):
        driver = self.driver
        if len(ifm) > 0:
            self.comeinifm(*ifm)
        listNameToValue = []
        for count in range(1, 41):
            strcount = '输入值' + str(count)
            if dict_data[strcount] == '':
                continue
            if len(dict_data[strcount].split('|')) < 2:
                continue
            listNameToValue.append(dict_data[strcount])

        self.logstu.debug(u'输入参数列表：')
        self.logstu.debug(listNameToValue)
        if len(listNameToValue) == 0:
            self.logstu.error(u'输入参数列表为空。')
            return

        for j in range(0, 10):
            try:
                tds = driver.find_elements(*self.editTds)
                break
            except UnexpectedAlertPresentException as e:
                self.logstu.debug(e)
                time.sleep(0.5)
        self.is_alert_and_close_and_get_text()

        len_list = len(listNameToValue)
        setnum_list = 0
        for i in range(0, len(tds)):
            if setnum_list >= len_list:
                self.logstu.debug(u'设置数据列表的所有数据循环设置完成。')
                break
            try:
                if self.all_type_to_encode(tds[i].text).strip() == '':
                    continue
            except UnexpectedAlertPresentException as e:
                self.logstu.error(self.close_alert_and_get_its_text())
                self.logstu.error(e)
            self.logstu.debug(u'当前td为：%s ==> 测试数据 %d : %s' % (tds[i].text.strip(),
                                                              setnum_list,
                                                              self.all_type_to_unicode(listNameToValue[setnum_list])))
            tdname = self.all_type_to_encode(listNameToValue[setnum_list]).split('|')[0]
            tdvalue = self.all_type_to_encode(listNameToValue[setnum_list]).split('|')[1]

            if self.all_type_to_encode(tds[i].text).strip().strip('*').strip() == tdname:
                setnum_list = setnum_list + 1
                # radios set
                try:
                    driver.implicitly_wait(0.5)
                    iradios = tds[i + 1].find_elements_by_css_selector('input[type="radio"]')
                    if len(iradios) > 0:
                        if tdvalue.split('+') > 1:
                            for rad_i in tdvalue.split('+'):
                                if int(rad_i) <= len(iradios):
                                    iradios[int(rad_i) - 1].click()
                        else:
                            iradios[int(tdvalue) - 1].click()
                        continue
                    driver.implicitly_wait(6)
                except NoSuchElementException as e:
                    driver.implicitly_wait(6)

                # checkbos set
                try:
                    driver.implicitly_wait(0.5)
                    icheckbos = tds[i + 1].find_elements_by_css_selector('input[type="checkbox"]')
                    if len(icheckbos) > 0:
                        if tdvalue.split('+') > 1:
                            for rad_i in tdvalue.split('+'):
                                if int(rad_i) <= len(icheckbos):
                                    icheckbos[int(rad_i) - 1].click()
                        else:
                            icheckbos[int(tdvalue) - 1].click()
                        continue
                    driver.implicitly_wait(6)
                except NoSuchElementException as e:
                    driver.implicitly_wait(6)

                editinput = tds[i + 1].find_element_by_css_selector('[class^=fftd]')
                if editinput.tag_name == 'input' and editinput.get_attribute('readonly') == None:
                    editinput.click()
                    editinput.clear()
                    editinput.send_keys(self.all_type_to_unicode(tdvalue))
                    continue
                if editinput.tag_name == 'select':
                    allOptions = editinput.find_elements_by_tag_name("option")
                    for v in allOptions:
                        if self.all_type_to_encode(v.text) == self.all_type_to_encode(tdvalue):
                            v.click()
                            break
                    continue
                if editinput.tag_name == 'input' and editinput.get_attribute('readonly') == 'true':
                    if tdname.find('日期') != -1 or tdname.find('时间') != -1:
                        timeinputid = editinput.get_attribute('id')
                        self.logstu.debug(u'日期 or 时间 输入控件 input id = ' + timeinputid)
                        js = 'document.getElementById("' + timeinputid + '").readOnly =false;'
                        driver.execute_script(js)
                        editinput.clear()
                        editinput.send_keys(self.all_type_to_unicode(tdvalue))
                        continue
                    selinput = tds[i + 1].find_element_by_css_selector(
                        'input[type="button"]')  # [class="inputdate"][value="..."]
                    oldhanlds = driver.window_handles
                    oldcurrent = driver.current_window_handle
                    self.thread_btn2(selinput)
                    self.logstu.debug(self.is_alert_and_close_and_get_text2())
                    self.goNewWindow(oldhanlds)

                    # 所属机构 选择使用的是 左侧菜单的方式，不是一般的表格式，需要特殊处理
                    if tdname == '所属机构':
                        self.leftMenuClick(tdvalue, 'ObjectList', 'left')
                        driver.switch_to_window(driver.current_window_handle)
                        self.table_BtnClick2(u'确认')
                        try:driver.switch_to_window(oldcurrent)
                        except Exception as e:
                            time.sleep(1)
                            driver.switch_to_window(oldcurrent)
                        if len(ifm) > 0:
                            self.comeinifm(*ifm)
                        continue

                    # 判断是否需要使用查询条件
                    if self.all_type_to_encode(tdvalue).find('[') != -1:
                        searchObj = self.all_type_to_encode(tdvalue).split('[')[1]
                        tdvalue = self.all_type_to_encode(tdvalue).split('[')[0]
                        self.comeinifm('ObjectList')
                        self.logstu.debug(u"在弹出的选择窗口中使用查询条件: " + self.all_type_to_unicode(searchObj))
                        self.selectAutoSets2(searchObj)
                    self.comeinifm('ObjectList', 'myiframe0')
                    self.table_RowClick(int(tdvalue))
                    newtitle = driver.title.strip()
                    self.logstu.debug(u'当前选择窗口的title为：' + newtitle)
                    if self.all_type_to_encode(newtitle) == '请选择所需信息':
                        driver.switch_to_window(driver.current_window_handle)
                        self.table_BtnClick2(u'确认')
                    else:
                        driver.switch_to_default_content()
                        self.comeinifm('ObjectList')
                        self.thread_btn(u'确认')
                        # self.table_BtnClick(u'确认')
                    try:
                        driver.switch_to_window(oldcurrent)
                    except:
                        self.logstu.debug('raise ResponseNotReady()')
                        time.sleep(1)
                        driver.switch_to_window(oldcurrent)
                    self.logstu.debug(u'当前窗体的title为：' + driver.title)
                    if len(ifm) > 0:
                        self.comeinifm(*ifm)
                    continue
                if editinput.tag_name == 'textarea' and editinput.get_attribute('readonly') == None:
                    editinput.clear()
                    editinput.send_keys(self.all_type_to_unicode(tdvalue))
                    continue
                if editinput.tag_name == 'textarea' and editinput.get_attribute('readonly') == 'true':
                    selinput = tds[i + 1].find_element_by_css_selector('input[class="inputdate"][value="..."]')
                    driver.set_page_load_timeout(2)
                    oldhanlds = driver.window_handles
                    oldcurrent = driver.current_window_handle
                    self.thread_btn2(selinput)
                    self.goNewWindow(oldhanlds)
                    self.comeinifm('ObjectList', 'myiframe0')
                    checks = driver.find_elements(*self.table_checkboxs)
                    for num in tdvalue.split('+'):
                        checks[int(num) - 1].click()
                    driver.switch_to_window(driver.current_window_handle)
                    self.table_BtnClick2(u'确认')
                    try:driver.switch_to_window(oldcurrent)
                    except:time.sleep(0.5);driver.switch_to_window(oldcurrent)
                    if len(ifm) > 0:
                        self.comeinifm(*ifm)
                    continue

    # 编辑页面所有数据的输入操作，保存和返回动作另外写，这里只填写
    def setEditTableValues(self,dict_data, *ifm):
        if len(ifm) > 0:
            self.comeinifm(*ifm)
        for count in range(1, 41):
            strcount = '输入值' + str(count)
            if dict_data[strcount] == '':
                continue
            sel_text = dict_data[strcount]

            self.logstu.debug(self.all_type_to_unicode(strcount) + u'|' + self.all_type_to_unicode(sel_text))
            if len(sel_text.split('|')) == 2:
                self.setEditTableValue(sel_text.split('|')[0], sel_text.split('|')[1], *ifm)

    def autoLogin(self, dict_data):
        if (dict_data["登录用户"] == "" or dict_data["登录密码"] == ""):
            return self.driver
        self.driver.implicitly_wait(5)
        self.driver.get(self.all_type_to_encode(dict_data["登录地址"]))
        self.loginact = LoginAct(self.driver)
        # 输入用户名
        user = self.all_type_to_encode(dict_data["登录用户"])
        if isinstance(user, float) :
            user = int(user)
        self.loginact.setLoginUser(user)
        # 输入密码
        self.loginact.setLoginPwd(self.all_type_to_encode(dict_data["登录密码"]))
        # 点击提交按扭
        self.loginact.clickSubmit()
        if self.is_alert_present(self.driver):
            try:
                alerttext = self.close_alert_and_get_its_text()
                #self.driver.switch_to_alert().accept()
                self.logstu.debug(u'登录后遇到弹窗，显示内容：\n\t'+ alerttext)
            except NoAlertPresentException as e:
                self.logstu.debug(u'登录后未遇到弹窗')
        return self.driver
    #获取alert文本  #add by limeng
    def get_alert_text(self):
        if self.is_alert_present2():
            try:
                alert = self.driver.switch_to_alert()
                alert_text = alert.text
                time.sleep(self.alertSleepTime)
                return alert_text
            except:
                return False
        else:
            return False
    # 获取alert文本  #add by limeng
    def alert_accept_dismiss(self,act):
        if self.is_alert_present2():
            try:
                alert = self.driver.switch_to_alert()
                time.sleep(self.alertSleepTime)
                if act =="accept": #self.accept_next_alert:
                    alert.accept()
                elif act =="dismiss":
                    alert.dismiss()
            except:
                return False
        else:
            return False
    # 判断是否有alert弹出窗
    def is_alert_present(self, drive_in):
        try:
            self.driver.switch_to.alert.text
            return True
        except NoAlertPresentException as e:
            return False


    # 判断是否有alert弹出窗
    def is_alert_present2(self):
        for i in range(0, 10):
            try:
                alstr = self.driver.switch_to.alert.text
                return True
            except NoAlertPresentException:
                return False
            except Exception as e:
                self.logstu.debug(e)
                time.sleep(1)


    # 关闭弹窗并获取显示的文本
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            time.sleep(self.alertSleepTime)
            if True:  #self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        except NoAlertPresentException as e:
            self.logstu.debug(e)
            return e
        finally:
            pass #self.accept_next_alert = True

    # 关闭弹窗并获取显示的文本
    def is_alert_and_close_and_get_text(self):
        if self.is_alert_present2():
            try:
                alert = self.driver.switch_to_alert()
                alert_text = alert.text.strip()
                time.sleep(self.alertSleepTime)
                if True:  # self.accept_next_alert:
                    alert.accept()
                else:
                    alert.dismiss()
                return alert_text
            except:
                return False
        else:
            return False

    def is_alert_and_close_and_get_text2(self):
        if self.is_alert_present2():
            try:
                alert = self.driver.switch_to_alert()
                alert_text = alert.text
                time.sleep(self.alertSleepTime)
                if True:  # self.accept_next_alert:
                    alert.accept()
                else:
                    alert.dismiss()
                return alert_text
            except:
                return 'False'
        else:
            return 'False'


    # 切换到（swich）新窗口，参数为新窗口的title
    def goNameWindow(self, winname1):
        winname = self.all_type_to_encode(winname1)
        driver = self.driver
        old = driver.current_window_handle
        windows = driver.window_handles
        self.logstu.debug(u'所有窗体的handles：' + ' '.join(windows)
                          + u'当前窗体的handle：' + old)
        for win in windows:
            if win == old:
                continue
            oldtitle = driver.title.strip()
            driver.switch_to_window(win)
            for gettitle in range(0, 6):
                newtitle = driver.title.strip()
                if oldtitle != newtitle:
                    break
                time.sleep(0.5)

            self.logstu.debug(u'跳转到窗体：' + win + u' | 窗体title：' + newtitle
                              + u' | 目标窗体title：' + self.all_type_to_unicode(winname))
            if self.all_type_to_encode(newtitle).find(winname) != -1:
                self.logstu.debug(u"成功切换到窗口：" + newtitle)
                return
            else:
                self.logstu.debug(u'当前窗体不是目标窗体，返回起始窗体 ' + old)
                driver.switch_to_window(old)

    # switch到新窗口，需要参数为旧窗口句柄列表
    # 用法，在打开新窗口操作前，获取 oldHandles = driver.window_handles，
    # 然后在打开新窗口后，下面方法会比较新旧两个窗口句柄列表，switch到新窗口中
    def goNewWindow(self, oldHandles):
        driver = self.driver
        for i in range(0, 10):
            try:
                current = driver.current_window_handle
                break
            except UnexpectedAlertPresentException as e:
                self.logstu.debug(e)
                self.logstu.debug('遇到Alert弹出窗口,切换到新窗口失败！')
                self.logstu.debug(self.is_alert_and_close_and_get_text())
                return False
            except Exception as e:
                self.logstu.debug(e)
                time.sleep(1)
        for lendiff in range(0, 10):
            try:
                if len(oldHandles) != len(driver.window_handles):
                    break
            except Exception as e:
                self.logstu.debug(e)
            time.sleep(0.5)

        for t in range(0, 10):
            try:windows = driver.window_handles
            except Exception as e:
                self.logstu.debug(e) # raise ResponseNotReady()
                time.sleep(0.5)
                continue

            mubiao = list(set(windows).difference(set(oldHandles)))
            self.logstu.debug(u'当前所有窗体的handles：' + ' '.join(windows)
                              + u'\n\t弹出窗体前所有旧窗体handles List：' + ' '.join(oldHandles)
                              + u'\n\t当前窗体的handle：' + current
                              + u'\n\t计算出来新窗体的handle：' + ' '.join(mubiao))
            if len(mubiao) == 1:
                for swtowin in range(0,10):
                    try:
                        driver.switch_to_window(mubiao[0])
                        self.logstu.debug(u"成功切换到窗体：" + driver.title)
                        return True
                    except Exception as e:
                        self.logstu.debug(e)
                        time.sleep(0.5)
            else:
                self.logstu.info(u"计算得到的新窗体有0个或多个，无法确定要跳转到哪个。")
                time.sleep(0.5)
        self.logstu.info(u"无法确定要跳转到哪个窗口")
        return False


    # 用于窗口按钮事件关闭后，切换回打开的窗口
    def goLastOneWindow(self):
        driver = self.driver
        windows = driver.window_handles
        self.logstu.debug(u'现存窗体：' + ' '.join(windows))
        driver.switch_to_window(windows[len(windows) - 1])
        try:
            self.logstu.debug(u'跳转到上述窗体列表的最后一个，' + driver.current_window_handle + ' | ' + driver.title)
        except:
            self.logstu.debug('raise ResponseNotReady()')
            time.sleep(1)
            self.logstu.debug(u'跳转到上述窗体列表的最后一个，' + driver.current_window_handle + ' | ' + driver.title)

    # 关闭当前窗口的方法，首先尝试调用关闭按钮click，如果该按钮不可见则直接调用窗口关闭api
    def winClose(self):
        driver = self.driver
        try:
            driver.find_element(*self.closeimg).click()
        except Exception as e:
            self.logstu.debug(e)
            self.logstu.debug(u'关闭窗体按钮不可见，调用driver.close()关闭')
            driver.close()
        newhs = driver.window_handles
        driver.switch_to_window(newhs[len(newhs) - 1])
        self.logstu.debug(u'关闭窗体后现有窗体：' + ' '.join(newhs)
                          + u'\n\t跳转到上述窗体List的最后一个：' + newhs[len(newhs) - 1])

    def winClose2(self):
        driver = self.driver
        beforewinnum = 0
        for i in range(0,5):
            try:
                beforewinnum = len(driver.window_handles)
                self.logstu.debug('winClose2 当前窗口数量:' + str(beforewinnum))
            except:
                self.logstu.debug(u'raise ResponseNotReady()')
                time.sleep(0.5)
            if beforewinnum > 1:
                driver.close()
                time.sleep(0.5)
                if len(driver.window_handles) == beforewinnum - 1:
                    self.logstu.debug(u'Close Window OK!')
                    break
                else:
                    time.sleep(0.5)
            else:
                self.logstu.info(u'当前只有1个窗体。')
        newhs = driver.window_handles
        driver.switch_to_window(newhs[len(newhs) - 1])

    def uploadfile(self, filename):
        driver = self.driver
        s = os.sep
        fileimg = os.path.abspath('.') + '\\images\\' + filename
        self.logstu.debug(u'待上传文件所在路径：' + fileimg)
        self.comeinifm('ObjectList')
        try:
            upelement = driver.find_element_by_name('AttachmentFileName')
        except Exception as e:
            self.logstu.debug(e)
            time.sleep(1)
            upelement = driver.find_element_by_name('AttachmentFileName')
        self.logstu.debug(upelement.tag_name)
        upelement.send_keys(fileimg)
        time.sleep(0.5)
        self.table_BtnClick2('确认')
        for i in range(0, 10):
            if self.is_alert_present2() == True:
                return self.close_alert_and_get_its_text()
            self.logstu.debug('上传文件确认，未找到弹出提示框，等待0.5秒。')
            time.sleep(0.5)
        return u'上传文件，确认按钮按下后未遇到Alert弹出确认框。'

    # 菜单选择
    def goto_menu(self, dict_data):
        driver = self.driver
        driver.set_page_load_timeout(15)
        menuList = []
        menuList.append(self.all_type_to_encode(dict_data["一级菜单"]))
        menuList.append(self.all_type_to_encode(dict_data["二级菜单"]))
        menuList.append(self.all_type_to_encode(dict_data["三级菜单"]))
        self.logstu.debug('菜单：%s - %s - %s' % (menuList[0],menuList[1],menuList[2]))

        for reclick in range(1, 11):
            for m in range(0, len(menuList)):
                if menuList[m] == '' and m == 0:
                    return
                try:
                    menu_ul = driver.find_element_by_css_selector('ul#ASMenuBar')
                    try:
                        opmenu = menu_ul.find_element_by_link_text(menuList[m])
                    except NoSuchElementException as e:
                        self.logstu.debug('未找到菜单(%s)，搜索 >> 标志查看是否存在' % (menuList[m]))
                        ActionChains(driver).move_to_element(menu_ul.find_element_by_link_text('>>')).perform()
                        break
                    ActionChains(driver).move_to_element(opmenu).perform()
                    self.logstu.debug('ActionChains MenuName :%s' % opmenu.text)
                    if m >= len(menuList) - 1:
                        opmenu.click()
                        return
                    if menuList[m + 1] == '':
                        opmenu.click()
                        return
                    time.sleep(1)
                except ElementNotVisibleException as e:
                    self.logstu.debug(e)
                    time.sleep(1)
                except NoSuchElementException as e:
                    self.logstu.debug(e)
                    wins = driver.window_handles
                    if len(wins) == 1:
                        driver.switch_to_default_content()
                    elif len(wins) > 1:
                        driver.close()
                        self.goLastOneWindow()
                    elif len(wins) == 0:
                        self.logstu.error('无可供操作的浏览器。')
                    time.sleep(1)
                except WebDriverException as e:
                    self.logstu.debug(e)
                    time.sleep(1)

    def noOneLogin(self, loginurl, inputuser, inputpwd):
        self.driver.delete_all_cookies()
        #self.driver = webdriver.Firefox()
        self.driver.get(loginurl)
        #self.driver.implicitly_wait(15)
        self.driver.find_element(By.NAME, 'UserID').clear()
        self.driver.find_element(By.NAME, 'UserID').send_keys(inputuser)
        self.driver.find_element(By.NAME, 'Password').send_keys(inputpwd)
        self.driver.find_element(By.CSS_SELECTOR, 'input.button_submit').click()
        alt = self.is_alert_and_close_and_get_text2()
        self.logstu.debug(alt)

    def onelogin_setpwd(self, loginurl, inputuser, oldpwd, newpwd):
        self.driver.find_element(By.ID, 'oldPassword').clear()
        self.driver.find_element(By.ID, 'oldPassword').send_keys(oldpwd)
        self.driver.find_element(By.ID, 'newPassword').send_keys(newpwd)
        self.driver.find_element(By.ID, 'newPassword2').send_keys(newpwd)
        self.driver.find_element(By.ID, 'buttonmiddletd21').click()
        alt = self.is_alert_and_close_and_get_text2()
        self.logstu.debug(alt)
        if self.all_type_to_encode(alt).find('密码修改成功') != -1:
            self.logstu.debug(inputuser + '|' + newpwd)
            self.noOneLogin(loginurl, inputuser, newpwd)
    # 测试输入数据唯一话，将月日时分数据替换掉(only)
    def testSateOnlySet(self, dict_data):
        for count in range(1, 41):
            strcount = '输入值' + str(count)
            if dict_data[strcount] == '':
                continue
            if dict_data[strcount].find('(only)') > -1:
                yrn = time.strftime("%m%d%H%M", time.localtime())
                dict_data[strcount] = dict_data[strcount].replace('(only)',yrn)
                self.logstu.debug(u'数据唯一化操作(only)替换为：%s' % (dict_data[strcount]))
        return dict_data
    # 查找输入数据中某一个值，找到第一个就返回
    def testDateSelect(self, dict_data, mubiao):
        for count in range(1, 41):
            strcount = '输入值' + str(count)
            if dict_data[strcount] == '':
                continue
            if self.all_type_to_encode(dict_data[strcount]).find(self.all_type_to_encode(mubiao)) > -1:
                return dict_data[strcount]
        return ''

    # 查找输入数据中包含某值的数据，返回一个列表
    def testDateSelectList(self, dict_data, mubiao):
        dataList = []
        for count in range(1, 41):
            strcount = '输入值' + str(count)
            if dict_data[strcount] == '':
                continue
            if self.all_type_to_encode(dict_data[strcount]).find(self.all_type_to_encode(mubiao)) > -1:
                dataList.append(dict_data[strcount])
        return dataList

    #根据字段名称获相应输入框中的值by zhuoshenghua
    def editTds_getValue(self,tdname1):
        driver = self.driver
        tdname = self.all_type_to_encode(tdname1)
        for j in range(0, 10):
            try:
                tds = driver.find_elements(*self.editTds)
                break
            except UnexpectedAlertPresentException as e:
                self.logstu.debug(e)
                time.sleep(0.5)
        for i in range(0, len(tds)):
            if self.all_type_to_encode(tds[i].text).strip().strip('*').strip() == self.all_type_to_encode(tdname):
                Values1=self.all_type_to_encode(tds[i].text).strip().strip('*').strip()
                self.logstu.info('Values1=%s'% Values1)
                editinput = tds[i + 1].find_element_by_css_selector('[class^=fftd]')
                if editinput.tag_name == 'input' and editinput.get_attribute('readonly') == None:
                    Values = editinput.get_attribute("value")
                    return Values
                    break

    #数据表中单元格输入内容   Add by zhuoshenghua
    def setTableCellValueFast(self, dict_data,row, *ifm):
        driver = self.driver
        if len(ifm) > 0:
            self.comeinifm(*ifm)
        listNameToValue = []
        for count in range(1, 41):
            strcount = '输入值' + str(count)
            if dict_data[strcount] == '':
                continue
            if len(dict_data[strcount].split('|')) < 2:
                continue
            listNameToValue.append(dict_data[strcount])

        self.logstu.debug(u'输入参数列表：')
        self.logstu.debug(listNameToValue)
        if len(listNameToValue) == 0:
            self.logstu.error(u'输入参数列表为空。')
            return

        len_list = len(listNameToValue)
        setnum_list = 0
        for i in range(0, len(listNameToValue)):
            colnum = int(self.all_type_to_encode(listNameToValue[setnum_list]).split('|')[0])
            tdvalue = self.all_type_to_encode(listNameToValue[setnum_list]).split('|')[1]
            rownum = int(row)
            self.logstu.info('colnum=%d,tdvalue=%s,rownum=%d'%(colnum,tdvalue,rownum))
            self.table_setValue(rownum,colnum,tdvalue)
            setnum_list = setnum_list+1

    # 选择指定行和列的单元格数据，参数为：
    #   rownum ：指定的行数，不包含标题行，从1开始
    #   colnum ：指定的的列数，不包含序号列，从1开始
    #   values ：表单中要输入的值
    #add by zhuoshenghua
    def table_selectValue(self, rownum, colnum,values):
        driver = self.driver
        trownum = self.table_getRowsCount()
        tcolnum = self.table_getColumnsCount()
        value = values
        if rownum > trownum :
            self.logstu.info(u'搜索的行数 '+ str(rownum) + u' 超过了实际表格行数' + str(trownum))
            return "NULL"
        if colnum > tcolnum:
            self.logstu.info(u'搜索的列数 ' + str(colnum) + u' 超过了实际表格列数' + str(tcolnum))
            return "NULL"
        table_tr = driver.find_elements(*self.table_tr)[rownum + 1] # 排除标题和隐藏行，参数rownum + 1就是需要的行标
        table_td = table_tr.find_elements_by_tag_name('td')[colnum]    # 第0列是序号列，数据列从1开始

        table_td.find_element_by_tag_name('input').send_keys(self.all_type_to_encode(value))

    # 选择页面中左（右）选择列表框中的数据移动到右（左）列表框中，参数为：
    #   dict_data ：用例中所要移动的数据
    #   btnname ：按钮名称
    #   titlename ：页面标题
    #   alerttext ：移动确认弹出提示信息
    #   iframe ：按钮所在的iframe
    #add by zhuoshenghua
    def Maintain(self,dict_data,btnname,titlename,alerttext,*iframe):
        btnName = btnname
        titleName = titlename
        left = 0
        right = 0
        rul = ''
        for count in range(1, 41):
            strcount = '输入值' + str(count)
            if dict_data[strcount] == '':
                continue
            sel_text = dict_data[strcount]
            self.logstu.debug(self.all_type_to_unicode(strcount) + u'|' + self.all_type_to_unicode(sel_text))
            if len(sel_text.split('|')) == 2:
                self.logstu.info(u'维护数据移动方向:%s,要移动的选项值：%s'% (sel_text.split('|')[0].strip(),sel_text.split('|')[1].strip()))
                if sel_text.split('|')[0].strip() == u'向右移':
                    self.comeinifm(*iframe)
                    self.driver.implicitly_wait(6)
                    self.table_BtnClick_NoSetTimeOut(btnName)
                    self.driver.implicitly_wait(6)
                    self.goNameWindow(titleName)
                    selects = self.driver.find_element_by_name('report_available')
                    selectvalue=selects.get_attribute("name")
                    self.logstu.info(u'选中选择框属性name：%s'% selectvalue)
                    allOptions = selects.find_elements_by_tag_name("option")
                    for option in allOptions:
                        if self.all_type_to_encode(option.text).strip() == sel_text.split('|')[1].strip():
                            self.logstu.info(u'选中记录%s'% self.all_type_to_encode(option.text).strip())
                            option.click()
                            break
                    self.driver.find_element_by_css_selector("img[name=\"movefrom_report_available\"]").click()
                    self.table_BtnClick3(u'确 定')
                    text = self.is_alert_and_close_and_get_text()
                    self.logstu.info(u"alert text is %s" % text)
                    if text ==alerttext:
                        self.logstu.info(u"%s向右移成功" % btnName)
                        right = right+1
                        self.logstu.info(u"第%s条数据向右移成功" % right)
                if sel_text.split('|')[0].strip() == u'向左移':
                    self.comeinifm(*iframe)
                    self.driver.implicitly_wait(6)
                    self.table_BtnClick_NoSetTimeOut(btnName)
                    self.driver.implicitly_wait(6)
                    self.goNameWindow(titleName)
                    selects = self.driver.find_element_by_name('report_chosen')
                    selectvalue=selects.get_attribute("name")
                    self.logstu.info(u'选中选择框属性name：%s'% selectvalue)
                    allOptions = selects.find_elements_by_tag_name("option")
                    for option in allOptions:
                        if self.all_type_to_encode(option.text).strip() ==  sel_text.split('|')[1].strip():
                            self.logstu.info(u'选中记录%s'% self.all_type_to_encode(option.text).strip())
                            option.click()
                            break
                    self.driver.find_element_by_css_selector("img[name=\"movefrom_report_chosen\"]").click()
                    self.table_BtnClick3(u'确 定')
                    text = self.is_alert_and_close_and_get_text()
                    self.logstu.info(u"alert text is %s" % text)
                    if text ==alerttext:
                        self.logstu.info(u"%s向左移成功" % btnName)
                        left = left+1
                        self.logstu.info(u"第%s条数据向左移成功" % left)
        if left <= 0 and right <= 0:
            self.logstu.info(u'未成功向右移动和向左移动任何一条记录，%s 失败'% (btnname))
            rul = u'失败'+'|'+str(left)+'|'+str(right)
            return rul
        else:
            self.logstu.info(u'成功向右移动%s条数据，成功向左移动%s条数据'% (right,left))
            rul = u'成功'+'|'+str(left)+'|'+str(right)
            return rul

class DriverInit(object):
    # 单例模式创建driver
    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super(DriverInit, cls).__new__(cls)
        return cls.instance

    def driver_init(self):
        #options = webdriver.ChromeOptions()
        #options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        #chromedriver = "C:\\Users\\xn045707\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe"
        #os.environ["webdriver.chrome.driver"] = chromedriver
        #self.driver = webdriver.Chrome(chrome_options=options)

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        return self.driver

class LoginAct():
    login_class = LoginElement()
    def   __init__(self, driver):
        self.driver = driver
        #self.driver = webdriver.Firefox()
    def setLoginUser(self, loginuser):
        self.driver.find_element(*self.login_class.userEdit).send_keys(loginuser)
    def setLoginPwd(self, loginpwd):
        self.driver.find_element(*self.login_class.passwdEdit).send_keys(loginpwd)
    def clickSubmit(self):
        driver = self.driver
        driver.find_element(*self.login_class.submitButton).click()

