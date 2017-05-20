# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

class LoginElement(object):
    #登录界面控件配置
    userEdit = (By.NAME, 'UserID')
    passwdEdit = (By.NAME,'Password')
    submitButton = (By.CLASS_NAME,'button_submit')
    resetButton = (By.CLASS_NAME,'button_reset')

class custLoginElement(object):
    #登录界面控件配置
    userEdit = (By.NAME, 'staffId')
    passwdEdit = (By.NAME,'passwd')
    submitButton = (By.ID,'loginButton')

class SalesmanApplyElement(object):
    addApplymenu = (By.LINK_TEXT,'新增的申请')
    approvalApplyingmenu = (By.LINK_TEXT,'审批中申请')
    approvalApplyagainmenu = (By.LINK_TEXT,'审批再次申请')
    approvalApplypassmenu = (By.LINK_TEXT,'审批通过申请')
    approvalApplyfailmenu = (By.LINK_TEXT,'审批失败申请')
    pass

# 查询条件
class PubSelectItemElement(object):
    ifm1 = (By.NAME, 'right')
    ifm2 = (By.NAME, 'rightup')                   # 查询条件所在iframe
    filterIconPlus = (By.ID, 'FilterIconPlus')   # 查询按钮前的 + img按钮
    filterIconMinus = (By.ID, 'FilterIconMinus') # 查询按钮前的 - img按钮
    # 查询条件所在表格, 名称在tr下的td[0], td[1]是select控件选择等于、以...开始等， td[2\3\4]需要判断是否输入框输入参数
    selectList = (By.CSS_SELECTOR, 'div#FilterArea >table >tbody >tr >td >div >table >tbody >tr')
    # 按钮列表，依次有 查询  清空  恢复  取消
    selectTabBtn = (By.CSS_SELECTOR, 'div#FilterArea >table >tbody >tr + tr >td >input')
    #selectSet = (By.CSS_SELECTOR, 'td >select')   # 查询条件列表，选择“等于、以...开始”

# 表格操作的公用方法
class PubTableItemElement(object):
    xntable = (By.CSS_SELECTOR, 'div#tableContainer >table')                   # 定位表格
    table_th = (By.CSS_SELECTOR, 'div#tableContainer >table >tbody >tr >th') # 标题th
    table_tr = (By.CSS_SELECTOR, 'div#tableContainer >table >tbody >tr')      # 表格所有行数
    table_btn = (By.CSS_SELECTOR, 'div.btn_text')     # 表格上的按钮 新增、详情等


class ProductCommodityCategoryElement(object):
    """A class for search results locators. All search results locators should come here"""
    pass

class SearchElement(object):
    #查询界面控件配置，供 QueryContractQuery使用
    customerNameEdit = (By.NAME, 'customerName')
    mobileNumberEdit = (By.NAME,'mobileNumber')
    idCardEdit = (By.NAME, 'idCard')
    idArtificialnoEdit = (By.NAME, 'idArtificialno')
#    submitButton = (By.CLASS_NAME,'button_submit')
    submitButton = (By.ID,'searchCustomerButton')
#    resetButton = (By.CLASS_NAME,'button_reset')
class FindElement(object):
    #详情页面定位元素，供QueryContractQuery使用
    ContractId = (By.XPATH, 'html/body/div/div/section/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td/div/a[1]')
class FindTableData(object):
    #详情页面定位元素，供QueryContractQuery
    TableData = (By.XPATH, 'html/body/div/div/section/div/div/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td/div[1]')