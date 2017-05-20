# -*- coding: utf-8 -*-
import cx_Oracle,logging,random,sys,time,xlrd

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from xlutils.copy import copy
from selenium.webdriver.common.keys import Keys

from Sys_CBS.PageObj.getElements import LoginElement
from Sys_CBS.PageObj.getElements import custLoginElement
from Utils.logger import Logger


class CommFunction:

    def __new__(cls, ):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super(CommFunction, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.mainwebdrive=''
        self.execldata = ""
        self.filepath = ""
        self.sheetname = ""
        self.table = ""
        self.appintable = ""
        self.logstu = Logger(sys.path[0] + '\\logs\\autotest.log', logging.DEBUG, logging.DEBUG)
        # self.ncpLogin = NCPTest()


    """存放一些公共的操作方法"""
    #启动浏览器
    def get_browserdrvie(self,browsertype):
        if browsertype == 'Chrome':
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
            return webdriver.Chrome(chrome_options=options)
        if browsertype == 'Firefox':
            return webdriver.Firefox()
        if browsertype == 'Ie':
            return webdriver.Ie()

    #读取testcase 数据 返回table
    def load_files(self,filepathname,sheetname):
        data = xlrd.open_workbook(filepathname)
        table=data.sheet_by_name(sheetname)
        self.execldata = copy(data)
        self.filepath = filepathname
        self.table = table
        self.appintable = data.sheet_by_name('appin')
        self.sheetname = sheetname
        return table

    #获取表格，列名对应的列
    def get_key_cell_col(self,keystr):
        label = 0
        ncols = self.table.ncols
        appinncols = self.appintable.ncols
        for i in range(ncols):
            strtemp2 = self.all_type_to_unicode(self.table.cell(0,i).value)
            keystr = self.all_type_to_unicode(keystr)
            if keystr == strtemp2:
                label = 1
                return i
        if label == 0 :
            for i in range(appinncols):
                strtemp2 = self.all_type_to_unicode(self.appintable.cell(0,i).value)
                keystr = self.all_type_to_unicode(keystr)
                if keystr == strtemp2:
                    label = 1
                    return i
            print ("没有取到： "+keystr+" ：对应的列数")
            sys.exit(0)

    #返回表格各列对应的列号
    def get_col_index(self):
        dict_col_index={
            "是否执行":self.get_key_cell_col('是否执行'),
            "操作类型":self.get_key_cell_col('操作类型'),
            "操作对象":self.get_key_cell_col('操作对象'),
            "执行时间":self.get_key_cell_col('执行时间'),
            "案例编号":self.get_key_cell_col('案例编号'),
            "案例名称":self.get_key_cell_col('案例名称'),
            "案例详情":self.get_key_cell_col('案例详情'),
            "预期结果":self.get_key_cell_col('预期结果'),
            "执行结果":self.get_key_cell_col('执行结果'),
            "验证结果":self.get_key_cell_col('验证结果'),
            "登录地址":self.get_key_cell_col('登录地址'),
            "登录用户":self.get_key_cell_col('登录用户'),
            "登录密码":self.get_key_cell_col('登录密码'),
            "环境":    self.get_key_cell_col('环境'),
            "子系统":  self.get_key_cell_col('子系统'),
            "主键索引":self.get_key_cell_col('主键索引'),
            "主键备注":self.get_key_cell_col('主键备注'),
            "一级菜单":self.get_key_cell_col('一级菜单'),
            "二级菜单":self.get_key_cell_col('二级菜单'),
            "三级菜单":self.get_key_cell_col('三级菜单'),
            "查询条件1":self.get_key_cell_col('查询条件1'),
            "查询条件2":self.get_key_cell_col('查询条件2'),
            "查询条件3":self.get_key_cell_col('查询条件3'),
            "查询条件4":self.get_key_cell_col('查询条件4'),
            "查询条件5":self.get_key_cell_col('查询条件5'),
            "查询条件6":self.get_key_cell_col('查询条件6'),
            "查询条件7":self.get_key_cell_col('查询条件7'),
        }
        for ii in range(1,8):
            selstr = '查询条件' + str(ii)
            dict_col_index[selstr] = self.get_key_cell_col(selstr)
        for ii in range(1,41):
            valstr = '输入值' + str(ii)
            dict_col_index[valstr] = self.get_key_cell_col(valstr)
        return dict_col_index
        for ii in range(1,8):
            selstr = 'sd查询条件' + str(ii)
            dict_col_index[selstr] = self.get_key_cell_col(selstr)
        for ii in range(1,41):
            valstr = 'sd输入值' + str(ii)
            dict_col_index[valstr] = self.get_key_cell_col(valstr)
        return dict_col_index

    #获取表每行对应的各列的相应的值
    def get_row_data(self,row_in):
        table_in = self.load_files(self.filepath,self.sheetname)
        dict_col_index = self.get_col_index()
        dict_row_data = {
            "是否执行":table_in.cell(row_in,dict_col_index['是否执行']).value,
            "操作类型":table_in.cell(row_in,dict_col_index['操作类型']).value,
            "操作对象":table_in.cell(row_in,dict_col_index['操作对象']).value,
            "执行时间":table_in.cell(row_in,dict_col_index['执行时间']).value,
            "案例编号":table_in.cell(row_in,dict_col_index['案例编号']).value,
            "案例名称":table_in.cell(row_in,dict_col_index['案例名称']).value,
            "案例详情": table_in.cell(row_in, dict_col_index['案例详情']).value,
            "预期结果":table_in.cell(row_in,dict_col_index['预期结果']).value,
            "执行结果":table_in.cell(row_in,dict_col_index['执行结果']).value,
            "验证结果":table_in.cell(row_in,dict_col_index['验证结果']).value,
            "登录地址":table_in.cell(row_in,dict_col_index['登录地址']).value,
            "登录用户":table_in.cell(row_in,dict_col_index['登录用户']).value,
            "登录密码":table_in.cell(row_in,dict_col_index['登录密码']).value,
            "环境":    table_in.cell(row_in, dict_col_index['环境']).value,
            "子系统":  table_in.cell(row_in, dict_col_index['子系统']).value,
            "主键索引":table_in.cell(row_in,dict_col_index['主键索引']).value,
            "主键备注":table_in.cell(row_in,dict_col_index['主键备注']).value,
            "一级菜单":table_in.cell(row_in,dict_col_index['一级菜单']).value,
            "二级菜单":table_in.cell(row_in,dict_col_index['二级菜单']).value,
            "三级菜单":table_in.cell(row_in,dict_col_index['三级菜单']).value
        }
        for ii in range(1,8):
            selstr = '查询条件' + str(ii)
            dict_row_data[selstr] = table_in.cell(row_in,dict_col_index[selstr]).value
        for ii in range(1,41):
            valstr = '输入值' + str(ii)
            dict_row_data[valstr] = table_in.cell(row_in,dict_col_index[valstr]).value

        #取有特殊标志的做处理
        for k in dict_row_data:
            findstr = self.all_type_to_unicode(dict_row_data[k])
            if isinstance(findstr,unicode):
                if ( '(rd' in findstr ) or ( '(up' in findstr ) or ( '(char' in findstr ):
                    dict_row_data[k] = self.set_cell_special_value(dict_row_data[k],row_in)
            if ('查询条件' in k) or ('输入值' in k ):
                col_str = "sd"+k
                col_in =  self.get_key_cell_col(col_str)
                self.write_file(dict_row_data[k],row_in,col_in)
        return dict_row_data

    #针对表格里各字段值的特殊处理
    def set_cell_special_value(self,str_in,row_in):
        col_in = 0
        newstr = ""
        str_in = str_in.split("|")
        for i in range(len(str_in)):
            #取随机数
            if '(rd' in str_in[i]:
                tp1_rd = str_in[i].split(")")
                rdnum = ""
                rdlaststr = ""
                if len(tp1_rd[0]) < 4:
                    print "你当前没有指定随机数位数  -->>  请在案例里指定"
                    continue
                else:
                    tp2_rd = tp1_rd[0].split("(")
                    tp_rd_bit = int(tp2_rd[1][2:])
                    tp_rd_max = 10**tp_rd_bit
                    rdnum = self.all_type_to_str((tp2_rd[0]) + str(random.randint(0,tp_rd_max)).zfill(tp_rd_bit))
                if len(tp1_rd) == 2:
                    rdlaststr = self.all_type_to_str(tp1_rd[1])
                    rdlaststr = rdlaststr.replace("$","")
                str_in[i] = rdnum + rdlaststr
            if '(char' in str_in[i]:
                chars =""
                tp1_rd = str_in[i].split(")")
                tp2_rd = tp1_rd[0].split("(")
                tp_rd_bit = int(tp2_rd[1][4:])
                for j in range(tp_rd_bit):
                    chars = chars + self.GB2312()
                str_in[i] = chars
            if '(up' in str_in[i]:
                tp1_upsd = str_in[i].split(")")
                if len(tp1_upsd) == 1:
                    print "你当前没有指定取向上哪一行的的标签少')'  -->>  请在案例里修改"
                    continue
                if len(tp1_upsd[0]) < 4 :
                    print "你当前没有指定取向上哪一行的数据  -->>  请在案例里指定(eg:本案例是:0行,上一条案例是:1行)"
                    continue
                if len(tp1_upsd) == 2:
                    tplast = tp1_upsd[1].split("$")
                    laststr = ""
                    if len(tplast) == 2:
                        tp1_upsd[1] = tplast[0]
                        laststr = self.all_type_to_str(tplast[1])
                    #取向上取的行数
                    tp1_upsd2 = tp1_upsd[0].split("(")
                    tp1_upsd_bit = int(tp1_upsd2[1][2:])
                    upsd_row = row_in - tp1_upsd_bit
                    #取向上取的列数
                    col_in = self.get_key_cell_col(tp1_upsd[1])
                    upsd_value = self.table.cell(upsd_row,col_in).value
                    tp1_upsd2[0] = self.all_type_to_str(tp1_upsd2[0])
                    upsd_value = self.all_type_to_str(upsd_value)
                    new_str = tp1_upsd2[0] + upsd_value + laststr
                    str_in[i] = new_str
        for j in range(len(str_in)):
            if j == len(str_in) - 1:
                newstr = self.all_type_to_str(newstr) +str_in[j]
            else:
                newstr = self.all_type_to_str(newstr) + self.all_type_to_str(str_in[j]) + "|"
        return newstr

        get_key_cell_col
    # 写数据到对应的表格中
    #str_in 表示要写到表格里的数据
    #row_in 表示要要写到表格对应的行数
    #col_in 表示要要写到表格对应的列数
    def write_file(self,str_in,row_in,col_in):
        data = xlrd.open_workbook(self.filepath)
        self.execldata = copy(data)
        newdatas = self.execldata
        newtable = newdatas.get_sheet(1)
        str_in = self.all_type_to_unicode(str_in)
        newtable.write(row_in,col_in,str_in)
        newdatas.save(self.filepath)

    #写验证结果
    def write_reslut(self,row_in):
        table_in = self.load_files(self.filepath,self.sheetname)
        expertstr = table_in.cell(row_in,self.get_key_cell_col("预期结果")).value
        runstr = table_in.cell(row_in,self.get_key_cell_col("执行结果")).value
        expertstr = self.all_type_to_str(expertstr)
        runstr = self.all_type_to_str(runstr)
        self.logstu.info("预期结果是:"+expertstr)
        self.logstu.info("执行结果是:"+runstr)
        exestr = ""
        if (expertstr in runstr ) or expertstr=="" :
            exestr = "PASS"
            self.write_file(exestr,row_in,self.get_key_cell_col("验证结果"))
        else:
            exestr = "FAIL"
            self.write_file(exestr,row_in,self.get_key_cell_col("验证结果"))
        return exestr

    #实时读取案例里的实时数据
    def get_cell_value(self,row_in,colname):
        table_in = self.load_files(self.filepath,self.sheetname)
        valuetstr = table_in.cell(row_in,self.get_key_cell_col(table_in,colname)).value
        return valuetstr

    #清空执行结果和sd开头的列 对应的值
    def clear_data(self):
        self.logstu.debug(u'testcase.xls数据清理')
        nrows = self.table.nrows
        appinnrows = self.appintable.nrows
        newtable = self.execldata.get_sheet(1)
        for i in range(1,nrows):
            for j in range(self.get_key_cell_col("sd查询条件1"),self.get_key_cell_col("sd输入值40")+1):
                newtable.write(i,j,"")
            newtable.write(i,self.get_key_cell_col("执行结果"),"")
            newtable.write(i,self.get_key_cell_col("验证结果"),"")
            newtable.write(i,self.get_key_cell_col("主键索引"),"")
        for j in range(1,appinnrows):
            newtable.write(i,self.get_key_cell_col("验证结果"),"")
            newtable.write(i,self.get_key_cell_col("返回报文"),"")
            newtable.write(i,self.get_key_cell_col("发送报文"),"")
        self.execldata.save(self.filepath)

    # 对传过来的 --按字符“|”拆分,返回一个队列数组
    def split_str(self, strs):
        value = strs.split("|")
        if len(value) == 2:
            value.append("")
        if len(value) == 1:
            value.append("")
            value.append("")
        return value

    #返回最低子菜单对应的菜单名
    def get_menuname(self,rows):
        menuname="" #最低子菜单对应的菜单名
        cols = self.get_key_cell_col("一级菜单")
        menu1 = self.table.cell(rows,cols).value
        menu2 = self.table.cell(rows,(cols+1)).value
        menu3 = self.table.cell(rows,(cols+2)).value
        menu1 = menu1.strip().encode("utf-8")
        menu2 = menu2.strip().encode("utf-8")
        menu3 = menu3.strip().encode("utf-8")
        return menu1,menu2,menu3

     #返回最低子菜单对应的菜单名
    def get_last_menuname(self,rows):
        menu1,menu2,menu3 = self.get_menuname(rows)
        if menu2 =="":
            menuname = menu1
        elif menu3 =="":
            menuname = menu2
        else:
            menuname = menu3
        return menuname

    # 菜单选择
    def goto_menu(self, webdr, rows):
        menu1,menu2,menu3 = self.get_menuname(rows)
        time.sleep(1)
        self.logstu.debug( '菜单：' + menu1 + ('' if menu2=='' else '-' + menu2) + ('' if menu3=='' else '-' + menu3))
        for reclick in range(1, 7):
            self.logstu.debug(str(reclick))
            if (menu1 != ""):
                opmenu1 = webdr.find_element_by_link_text(menu1)
                if (menu2 == ""):
                    opmenu1.click()
                    break
                else:
                    self.logstu.debug('光标移到工一级菜单上:')
                    ActionChains(webdr).move_to_element(opmenu1).perform()
                    time.sleep(2)
                    try:
                        self.logstu.debug('查找二级菜单:')
                        opmenu2 = webdr.find_element_by_link_text(menu2)
                    except NoSuchElementException as e:
                        self.logstu.debug("未找到二级菜单【" + menu2 + "】重试第" + str(reclick) + "次")
                        time.sleep(3)
                        continue
                    if (menu3 == ""):
                        self.logstu.debug('点击二级菜单:')
                        opmenu2.click()
                        break
                    else:
                        ActionChains(webdr).move_to_element(opmenu2).perform()
                        time.sleep(2)
                        try:
                            opmenu3 = webdr.find_element_by_link_text(menu3)
                        except NoSuchElementException as e:
                            self.logstu.debug("未找到三级菜单【" + menu3 + "】重试第" + str(reclick) + "次")
                            time.sleep(3)
                            continue
                        opmenu3.click()
                        time.sleep(1)
                        break

    #菜单对应相应的脚本名称
    def get_menu_to_script(self):
        dict_menu_to_script = {
        ### CBS 系统 ###
            "登录": "Sys_CBS.TestClass.login|Login",
            "商品贷产品系列": "Sys_CBS.TestClass.product_Line_CommodityLoan|ProductLineCommodityLoan",
            "现金贷产品系列": "Sys_CBS.TestClass.product_Line_CashLoan|ProductLineCashLoan",
            "销售人员入职申请": "Sys_CBS.TestClass.salesman_Apply|SalesmanApply",
            "销售人员入职审核": "Sys_CBS.TestClass.salesman_CheckApply|SalesmanCheckApply",
            "商户门店准入申请": "Sys_CBS.TestClass.channel_RetailStore_RetailStoreApply|ChannelRetailStoreRetailStoreApply",
            "商户门店准入审批": "Sys_CBS.TestClass.channel_RetailStore_RetailStoreApprove|ChannelRetailStoreRetailStoreApprove",
            "退款审批": "Sys_CBS.TestClass.afterLoan_RefundApprove|AfterLoanRefundApprove",
            "退保审批": "Sys_CBS.TestClass.afterLoan_WithdrawInsuranceApprove|AfterLoanWithdrawInsuranceApprove",
            "合同查询": "Sys_CBS.TestClass.statisticalQuery_ContractQuery|StatisticalQueryContractQuery",
            "期款协议上传": "Sys_CBS.TestClass.afterLoan_PaymentAgreementUpload|AfterLoanPaymentAgreementUpload",
            "期款豁免录入": "Sys_CBS.TestClass.afterLoan_TermAmtExemptionApply|AfterLoanTermAmtExemptionApply",
            "期款豁免复核": "Sys_CBS.TestClass.afterLoan_TermAmtExemptionApprove|AfterLoanTermAmtExemptionApprove",
            "门店管理": "Sys_CBS.TestClass.channel_RetailStore_Store|ChannelRetailStoreStore",
            "培训结果登记": "Sys_CBS.TestClass.salesman_TrainingResults|SalesmanTrainingResults",
            "用户管理": "Sys_CBS.TestClass.system_User|SystemUser",
            "退货审批": "Sys_CBS.TestClass.afterLoan_SalesReturnApprove|AfterLoanSalesReturnApprove",
            "商品贷产品配置": "Sys_CBS.TestClass.product_Config_CommodityLoan|ProductConfigCommodityLoan",
            "现金贷产品配置": "Sys_CBS.TestClass.product_Config_CashLoan|ProductConfigCashLoan",
            "费用维护": "Sys_CBS.TestClass.product_CostType|ProductCostType",
            "商品类型": "Sys_CBS.TestClass.product_Type|ProductType",
            "核算交易定义": "Sys_CBS.TestClass.product_AccountingConfig_Transaction|ProductAccountingConfigTransaction",
            "账务代码定义": "Sys_CBS.TestClass.product_AccountingConfig_AccountCode|ProductAccountingConfigAccountCode",
            "影像类型配置": "Sys_CBS.TestClass.product_ImageTypeConfig|ProductImageTypeConfig",
            "门店准入申请": "Sys_CBS.TestClass.channel_RetailStore_StoreApply|ChannelRetailStoreStoreApply",
            "门店准入审批": "Sys_CBS.TestClass.channel_RetailStore_StoreApprove|ChannelRetailStoreStoreApprove",
            "商户信息变更申请": "Sys_CBS.TestClass.channel_RetailStore_RetailChangeApply|ChannelRetailStoreRetailChangeApply",
            "商户信息变更审核": "Sys_CBS.TestClass.channel_RetailStore_RetailChangeApprove|ChannelRetailStoreRetailChangeApprove",
            "门店信息变更申请": "Sys_CBS.TestClass.channel_RetailStore_StoreChangeApply|ChannelRetailStoreStoreChangeApply",
            "门店信息变更审核": "Sys_CBS.TestClass.channel_RetailStore_StoreChangeApprove|ChannelRetailStoreStoreChangeApprove",
            "商户管理": "Sys_CBS.TestClass.channel_RetailStore_Retail|ChannelRetailStoreRetail",
            "门店设备申请": "Sys_CBS.TestClass.channel_RetailStore_StoreEquipmentApply|ChannelRetailStoreStoreEquipmentApply",
            "门店设备申请审核": "Sys_CBS.TestClass.channel_RetailStore_StoreEquipmentApprove|ChannelRetailStoreStoreEquipmentApprove",
            "银行账号申请": "Sys_CBS.TestClass.channel_BankAccount_Apply|ChannelBankAccountApply",
            "银行账号审批": "Sys_CBS.TestClass.channel_BankAccount_Approve|ChannelBankAccountApprove",
            "银行代码管理": "Sys_CBS.TestClass.channel_BankCode|ChannelBankCode",
            "代扣渠道维护": "Sys_CBS.TestClass.channel_withholdChannel|ChannelwithholdChannel",
            "保险供应商管理": "Sys_CBS.TestClass.channel_InsuranceSupplier|ChannelInsuranceSupplier",
            "销售人员信息变更申请": "Sys_CBS.TestClass.salesman_ChangeApply|SalesmanChangeApply",
            "销售人员变更审核": "Sys_CBS.TestClass.salesman_CheckChangeApply|SalesmanCheckChangeApply",
            "贷款审批": "Sys_CBS.TestClass.loan_Approve|LoanApprove",
            "流程监控": "Sys_CBS.TestClass.loan_ProcessMonitoring|LoanProcessMonitoring",
            "合同撤销": "Sys_CBS.TestClass.loan_Contract_VoidableContract|LoanContractVoidableContract",
            "批量付款管理": "Sys_CBS.TestClass.financial_BatchPay|FinancialBatchPay",
            "合同冻结付款管理": "Sys_CBS.TestClass.financial_ContractFreezingPay|FinancialContractFreezingPay",
            "退款登记": "Sys_CBS.TestClass.financial_RefundApply|FinancialRefundApply",
            "退款复核": "Sys_CBS.TestClass.financial_RefundReview|FinancialRefundReview",
            "退货登记": "Sys_CBS.TestClass.financial_SalesReturnApply|FinancialSalesReturnApply",
            "小牛在线每日放款检查": "Sys_CBS.TestClass.financial_XIAONIUEveryDayLoanCheck|FinancialXIAONIUEveryDayLoanCheck",
            "合作机构每日放款检查": "Sys_CBS.TestClass.financial_CooperationEveryDayLoanCheck|FinancialCooperationEveryDayLoanCheck",
            "代扣账号变更审批": "Sys_CBS.TestClass.afterLoan_WithholdAccountChangeApprove|AfterLoanWithholdAccountChangeApprove",
            "强制还款": "Sys_CBS.TestClass.afterLoan_ForceRepayment|AfterLoanForceRepayment",
            "商户查询": "Sys_CBS.TestClass.statisticalQuery_RetailQuery|StatisticalQueryRetailQuery",
            "门店查询": "Sys_CBS.TestClass.statisticalQuery_StoreQuery|StatisticalQueryStoreQuery",
            "销售合同查询": "Sys_CBS.TestClass.statisticalQuery_SalesContractQuery|StatisticalQuerySalesContractQuery",
            "还款文件查询": "Sys_CBS.TestClass.statisticalQuery_RepaymentDocQuery|StatisticalQueryRepaymentDocQuery",
            "代扣记录查询": "Sys_CBS.TestClass.statisticalQuery_WithHoldReCord|StatisticalQueryWithHoldReCord",
            "销售信息查询": "Sys_CBS.TestClass.statisticalQuery_SalesInfoQuery|StatisticalQuerySalesInfoQuery",
            "部门管理": "Sys_CBS.TestClass.system_Department|SystemDepartment",
            "角色管理": "Sys_CBS.TestClass.system_Role|SystemRole",
            "综合信息": "Sys_CBS.TestClass.system_Synthesis|SystemSynthesis",
            "自动豁免参数维护": "Sys_CBS.TestClass.parameter_AutoExemptSum|ParameterAutoExemptSum",
            "代码管理": "Sys_CBS.TestClass.parameter_CodeManage|ParameterCodeManage",
            "审批配置": "Sys_CBS.TestClass.parameter_AuditConfig|ParameterAuditConfig",
            "方法配置": "Sys_CBS.TestClass.parameter_MethodConfig|ParameterMethodConfig",
            "取消合同参数": "Sys_CBS.TestClass.parameter_CancleContract|ParameterCancleContract",
            "错误类型参数": "Sys_CBS.TestClass.parameter_ErrorType|ParameterErrorType",
            "app秒拒延时参数配置": "Sys_CBS.TestClass.parameter_ConsumerLoan_AppSecondsfromDelay|ParameterConsumerLoanAppSecondsfromDelay",
            "黑名单管理": "Sys_CBS.TestClass.parameter_ConsumerLoan_BlackList|ParameterConsumerLoanBlackList",
            "优质雇主名单管理": "Sys_CBS.TestClass.parameter_ConsumerLoan_HighQualityEmployerList|ParameterConsumerLoanHighQualityEmployerList",
            "社保信息查询维护": "Sys_CBS.TestClass.parameter_ConsumerLoan_SocialInfoQuery|ParameterConsumerLoanSocialInfoQuery",
            "临近城市维护": "Sys_CBS.TestClass.parameter_ConsumerLoan_NearCityManage|ParameterConsumerLoanNearCityManage",
            "门店分组代码维护": "Sys_CBS.TestClass.parameter_ConsumerLoan_StoreGroupCodeManage|ParameterConsumerLoanStoreGroupCodeManage",
            "超期未注册期限配置": "Sys_CBS.TestClass.parameter_ConsumerLoan_ExpiredRegisteManage|ParameterConsumerLoanExpiredRegisteManage",
            "提前还款申请提前天数配置": "Sys_CBS.TestClass.parameter_ConsumerLoan_PrepaymentApplyDayManage|ParameterConsumerLoanPrepaymentApplyDayManage",
            "CFCA身份验证配置": "Sys_CBS.TestClass.parameter_ConsumerLoan_CFCACertIDManage|ParameterConsumerLoanCFCACertIDManage",
            "GSPN维护": "Sys_CBS.TestClass.parameter_ConsumerLoan_GSPNManage|ParameterConsumerLoanGSPNManage",
            "流程阶段审核要点": "Sys_CBS.TestClass.parameter_ConsumerLoan_AuditPoints_ProcessStage|ParameterConsumerLoanAuditPointsProcessStage",
            "自动取消合同天数维护": "Sys_CBS.TestClass.parameter_ConsumerLoan_AutoCancleContract|ParameterConsumerLoanAutoCancleContract",
            "短信模板配置": "Sys_CBS.TestClass.parameter_ConsumerLoan_SMSModelConfig|ParameterConsumerLoanSMSModelConfig",
            "Pad参数配置": "Sys_CBS.TestClass.parameter_ConsumerLoan_PadParameterConfig|ParameterConsumerLoanPadParameterConfig",
            "第三方接口参数配置": "Sys_CBS.TestClass.parameter_ConsumerLoan_ThirdPartyInterface|ParameterConsumerLoanThirdPartyInterface",
            "规则引擎配置": "Sys_CBS.TestClass.parameter_ConsumerLoan_RulesEngine|ParameterConsumerLoanRulesEngine",
            "app进件": "Sys_CBS.TestClass.app_In|AppIn",
            "sql": "Sys_CBS.TestClass.sqloption|Sqloption",
            "信息验证": "Sys_CBS.TestClass.merchant_InformationVerification|MerchantInformationVerification",
            "电销规则策略": "Sys_CBS.TestClass.marketing_rule_strategy|marketing_rule_strategy",
            "营销活动定义": "Sys_CBS.TestClass.marketing_activity_definition|marketing_activity_definition",
            "短信推广策略": "Sys_CBS.TestClass.marketing_SMS_strategy|marketing_SMS_strategy",
            "微信推广策略": "Sys_CBS.TestClass.marketing_WeChat_strategy|marketing_WeChat_strategy",
            "渠道管理": "Sys_CBS.TestClass.marketing_channel_management|marketing_channel_management",
        ### Cust 系统 ###
            "客户查询": "Sys_Cust.TestCase.Query_ContractQuery|QueryContractQuery",
        ### NCP 系统 ###
            "NCP登录": "Sys_NCP.TestClass.TestLogin|TestLogin",
            "NCP_Function": "Sys_NCP.TestClass.DBCase.NCP_DB_Function|NCP_DB_Function",
            "主页面检查": "Sys_NCP.TestClass.DBCase.checkMainPageElement|checkMainPageElement",
            "页面元素检查": "Sys_NCP.TestClass.DBCase.checkPageElement|checkPageElement",
            "单条件查询": "Sys_NCP.TestClass.DBCase.SingleConditionQuery|SingleConditionQuery",
            "组合条件查询": "Sys_NCP.TestClass.DBCase.CombinationConditionQuery|CombinationConditionQuery",
            "对表单记录操作": "Sys_NCP.TestClass.DBCase.FormOperation|FormOperation"
        }
        return dict_menu_to_script

    def is_alert_present(self,drive_in):
        try: drive_in.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def all_type_to_unicode(self,str_in):
        #处理字符编码问题
        if isinstance(str_in, float):
            str_in = int(str_in)
        elif isinstance(str_in, unicode):
            pass
        else:
            str_in = unicode(str_in,"utf-8")
        return str_in

    def all_type_to_str(self,str_in):
        #处理字符编码问题
        if isinstance(str_in, float):
            str_in = str(int(str_in))
        elif isinstance(str_in, unicode):
            str_in = str_in.encode("utf-8")
        return str_in

    #登录
    def login_success(self,subsystem_in,login_url_in,username_in,passwd_in,browserName):
        #处理字符编码问题
        subsystem_in = self.all_type_to_unicode(subsystem_in)
        username_in = self.all_type_to_unicode(username_in)
        passwd_in = self.all_type_to_unicode(passwd_in)
        #启动浏览器
        # driver = self.get_browserdrvie('Firefox')
        driver = self.get_browserdrvie(browserName)
        driver.get(login_url_in)
        time.sleep(1)
        if subsystem_in == 'cust':
            driver.find_element(*custLoginElement.userEdit).send_keys(username_in)#输入用户登录名
            driver.find_element(*custLoginElement.passwdEdit).send_keys(passwd_in)#输入密码
            driver.find_element(*custLoginElement.submitButton).click()#点击提交按扭
        elif subsystem_in == 'ncp':
            # self.ncpLogin.login(username_in,passwd_in,login_url_in)
            elem = driver.find_element_by_id("loginname")
            elem.clear()
            elem.send_keys(username_in)
            elem = driver.find_element_by_id("password")
            elem.clear()
            elem.send_keys(passwd_in)
            elem = driver.find_element_by_name("登录")
            elem.send_keys(Keys.RETURN)
            time.sleep(1)
        else:
            driver.find_element(*LoginElement.userEdit).send_keys(username_in)#输入用户登录名
            driver.find_element(*LoginElement.passwdEdit).send_keys(passwd_in)#输入密码
            driver.find_element(*LoginElement.submitButton).click()#点击提交按扭
        #将webdrive传回给主调用函数
        self.mainwebdrive = driver
        if self.is_alert_present(driver):
            try:driver.switch_to_alert().accept()
            except NoAlertPresentException as e: print 'NoAlertPresentException: login switch_to_alert'
        return driver

    def reslut_log_report(self):
        table = self.load_files(self.filepath,self.sheetname)
        exelabel = 0
        reslabel = 0
        self.logstu.info(u"案例名称 -->> 预期结果 -->> 执行结果 -->> 验证结果")
        for i in range(table.nrows):
            if (table.cell(i,self.get_key_cell_col(u"是否执行")).value == u'是') and (table.cell(i,self.get_key_cell_col(u"操作类型")).value <> u'sql'):
                testname = self.all_type_to_str(table.cell(i,self.get_key_cell_col(u"案例名称")).value)
                yqreslut = self.all_type_to_str(table.cell(i,self.get_key_cell_col(u"预期结果")).value)
                exreslut = self.all_type_to_str(table.cell(i,self.get_key_cell_col(u"执行结果")).value)
                yzreslut = self.all_type_to_str(table.cell(i,self.get_key_cell_col(u"验证结果")).value)
                self.logstu.info(testname+'           '
                                 +yqreslut+'           '
                                 +exreslut+'           '
                                 +yzreslut)
                exelabel +=1
                if (table.cell(i,self.get_key_cell_col("验证结果")).value == 'PASS'):
                    reslabel +=1
        #self.logstu.info("总的")

    def oracle_opt(self,connstr,sqlstr):
        #sqlstr = "select serialno from xiaoniu.call_rule_info where rownum <2"
        sqlstr = sqlstr.replace(";","")
        conn = cx_Oracle.connect(connstr)
        sqlstr = sqlstr.replace('"',"'")
        self.logstu.debug(u"数据库连接串是: " + connstr)
        self.logstu.debug(u"数据库SQL语句是: " + sqlstr)
        cursor = conn.cursor()
        cursor.execute(sqlstr)
        conn_res_str = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        if 'select' in sqlstr[0:8]:
            self.logstu.debug(u'sql执行返回结果是' + str(conn_res_str))
            conn_res_str = str(conn_res_str).split(")")[0]
            conn_res_str = conn_res_str.split("'")
            #self.logstu.debug(conn_res_str)
            sqlvalue = ""
            for ts in range(1,len(conn_res_str),2):
                sqlvalue = sqlvalue + conn_res_str[ts] + "|"
            conn_res_str = sqlvalue[:-1]
        self.logstu.debug(u'处理完后保存字符串是' + str(conn_res_str))
        return conn_res_str



