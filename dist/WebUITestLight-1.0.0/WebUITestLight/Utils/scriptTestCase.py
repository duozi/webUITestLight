# -*- coding: utf-8 -*-

class scriptTestCase():
    '''脚本用例'''

    def get_scriptTestCaseList(self):
        TestCaseList = [
            {'case_num': 'test001', 'test_order': '0001', 'is_run':1, 'ModuleName': 'Sys_Carloan.TestClass.TestAdmin','ClassName': 'TestAdmin', 'case_title': 'CarLoan Page Check', 'case_details': 'Admin All Page Check'},
            {'case_num': 'ContractQuery001', 'test_order': '1001', 'is_run':1,'ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3144_NCP5','ClassName': 'checkMainPageElement', 'case_title': '合同管理', 'case_details': '验证主界面的界面元素'},
            {'case_num': 'ContractQuery002', 'test_order': '1002', 'is_run':0,'ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3145_NCP5','ClassName': 'checkContractQueryPageElement', 'case_title': '合同查询', 'case_details': '合同查询_页面元素识别'},
            {'case_num': 'ContractQuery003', 'test_order': '1003', 'is_run':0,'ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3146_NCP6', 'ClassName': 'ContractQuery_SingleCondition','case_title': '合同查询', 'case_details': '查询功能-单个条件查询功能'},
            {'case_num': 'ContractQuery004', 'test_order': '1004', 'is_run':0,'ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3147_NCP6','ClassName': 'ContractQuery_CombinationCondition', 'case_title': '合同查询','case_details': '合同查询_组合条件查询'},
            # {'case_num': 'ContractQuery005', 'test_order': '1005', 'is_run': 1,'ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3148_NCP8','ClassName': 'ContractQuery_FormOperation', 'case_title': '合同查询', 'case_details': '合同查询_对表单数据操作'},
            # {'case_num': 'test001', 'test_order': '0001', 'is_run':1, 'ModuleName': 'Sys_NCP.TestClass.TestLogin','ClassName': 'TestLogin', 'case_title': '登录', 'case_details': '登录成功'},
            {'case_num': 'test002', 'test_order': '0002','is_run':1, 'ModuleName': 'Sys_NCP.TestClass.Test2', 'ClassName': 'Test2','case_title': '案例标题2', 'case_details': '案例详细内容2'},
            {'case_num': 'test003', 'test_order': '0003','is_run':1, 'ModuleName': 'Sys_NCP.TestClass.ContractQuery','ClassName': 'ContractQuery', 'case_title': '合同管理', 'case_details': '合同查询'},
            {'case_num': 'test004', 'test_order': '0004','is_run':1, 'ModuleName': 'Sys_NCP.TestClass.SysManage','ClassName': 'SysManage', 'case_title': '系统管理', 'case_details': '角色管理'},
            {'case_num': 'test005', 'test_order': '0005','is_run':1, 'ModuleName': 'Sys_NCP.TestClass.CountManage','ClassName': 'CountManage', 'case_title': '账户管理', 'case_details': '账户综合信息查询'},
            # {'case_num': 'ContractQuery005', 'test_order': '1005', 'is_run': 1,'ModuleName': 'Sys_NCP.TestClass.ContractManage.ContractQuery.XN3148_NCP8','ClassName': 'ContractQuery_FormOperation', 'case_title': '合同查询', 'case_details': '合同查询_对表单数据操作'},
        ]
        return TestCaseList


    def get_checkMainPageElementTestData(self):
        DataList = [
            {'menuName_one':'合同管理','menuName_two':'合同查询','LocationMethod':'页面元素名称','LocationValue':'合同查询','截图名称':'合同管理_合同查询'},
            # {'menuName_one':'合同管理','menuName_two':'可撤销合同查询','LocationMethod':'页面元素id','LocationValue':'RETAIL_NO','截图名称':'合同管理_可撤销合同查询'},
            {'menuName_one':'合同管理','menuName_two':'合同撤销','LocationMethod':'页面元素名称','LocationValue':'合同撤销','截图名称':'合同管理_合同撤销'},
        ]
        return DataList

    def get_checkPageElementTestData(self):
        DataList = [
         #   {'menuName_one':'合同管理','menuName_two':'合同查询', 'checkMethod': 'textName','LocationMethod': 'span','LocationValue': '客户名称,合同编号,身份证号码,合同申请日期,合同签署日期,合同激活日期,送货状态,产品系列,商户代码,门店代码,门店名称,SA/RA代码,SA/RA姓名,销售经理ID,销售经理姓名,是否参加保险,是否购买灵活还款服务包,合同状态,销售省份,销售城市,合作机构','截图名称': '合同查询_查询条件字段检查'},
            {'menuName_one':'合同管理','menuName_two':'合同查询', 'checkMethod': 'table', 'LocationMethod': 'th','LocationValue': '客户名称,合同编号,合同状态,身份证号,手机号,合同申请日期,合同激活日期,贷款本金,合同总金额,分期期数,每月还款额,是否购买,灵活还款包,是否,参加保险,门店代码,商户代码', '截图名称': '合同查询页_列表字段检查'},
            {'menuName_one': '合同管理', 'menuName_two': '合同查询', 'checkMethod': 'link', 'LocationMethod': 'a','LocationValue': '合同详情,电子合同调阅,合同影像调阅,协议详情,退货申请,豁免申请,退保申请,提现申请,提前还款申请,退款申请,变更还款日,取消灵活还款服务包,结清证明打印,导出Excel','截图名称': '合同查询页_连接字段检查'},
            {'menuName_one': '合同管理', 'menuName_two': '合同查询', 'checkMethod': 'button', 'LocationMethod': 'button','LocationValue': '搜索','截图名称': '合同查询页_按钮字段检查'}

        ]
        return DataList

    def get_ContractQuery_SingleConditionTestData(self):
        DataList = [
            {'LocationClass':'输入框','LocationMethod':'输入框提示','LocationValue':'输入客户名称','FillingValue':'暴发户','截图名称':'合同查询_客户名称查询'},
            # {'LocationClass':'日期','LocationMethod': '输入框id', 'LocationValue': 'INPUT_DATE_BEGIN', 'FillingValue': '2016-12-12','截图名称':'合同查询_申请开始时间查询'},
            # {'LocationClass': '日期', 'LocationMethod': '输入框id', 'LocationValue': 'INPUT_DATE_END','FillingValue': '2016-12-12','截图名称':'合同查询_申请结束时间查询'},
            {'LocationClass': '下拉选项', 'LocationMethod': '输入框id', 'LocationValue': 'PRODUCT_TYPE','FillingValue': '商品贷','截图名称':'合同查询_商品类型查询'}
        ]
        return DataList

    def get_ContractQuery_CombinationConditionTestData(self):
        DataList = [ #日期输入框id|INPUT_DATE_BEGIN|2016-10-12,日期输入框id|INPUT_DATE_END|2016-12-12
            {'menuName_one': '合同管理', 'menuName_two': '合同查询', 'QueryMethod': 'CombinationCondition','LocationValue': '输入框提示|输入客户名称|暴发户','截图名称': '合同查询页_组合条件检查'},
            {'menuName_one': '合同管理', 'menuName_two': '合同查询', 'QueryMethod': 'CombinationCondition','LocationValue': '输入框id|STORE_CODE|P5e0021,下拉选择框id|CONTRACT_STATUS_TYPE|现行','截图名称': '合同查询页_组合条件(输入框+日期+下拉框)检查'},
        ]
        return DataList

    def get_ContractQuery_FormOperationTestData(self):
        DataList = [  #,电子合同调阅|2,合同影像调阅|1
            {'menuName_one': '合同管理', 'menuName_two': '合同查询', 'OperationMethod': 'FormOperation','LocationValue': '退款申请|1,变更还款日|1','截图名称': '合同查询页_对表单值操作'},
            {'menuName_one': '合同管理', 'menuName_two': '合同查询', 'OperationMethod': 'FormOperation','LocationValue': '合同详情|0,电子合同调阅|2,合同影像调阅|1','截图名称': '对表单操作'},
            {'menuName_one': '合同管理', 'menuName_two': '合同查询', 'OperationMethod': 'FormOperation','LocationValue': '协议详情|1,退货申请|1,豁免申请|1,退保申请|1,提现申请|1,提前还款申请|1,退款申请|1,变更还款日|1,取消灵活还款服务包|1,结清证明打印|1','截图名称': '合同查询页_对表单值操作'},
            # {'menuName_one': '合同管理', 'menuName_two': '合同查询', 'OperationMethod': 'FormOperation','LocationValue': '合同详情|1,电子合同调阅|2,合同影像调阅|1,协议详情|1,退货申请|1,豁免申请|1,退保申请|1,提现申请|1,提前还款申请|1,退款申请|1,变更还款日|1,取消灵活还款服务包|1,结清证明打印|1,导出Excel|1','截图名称': '合同查询页_对表单值操作'},
        ]
        return DataList