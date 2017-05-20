# -*- coding: utf-8 -*-

from Sys_CBS.PageObj.lyElementsOperation import PublicAct
import unittest

class Sqloption(unittest.TestCase):
    dict_data = ''   #接收main脚本传过来的参数
    mainWebDr=""     #接收main脚本付过来的
    comm = ""        #接收main脚本传送的公共类实例对象
    row =""          #接收main脚本传送的当前处理的行数
    #页面控件元素别
    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_AfterLoanPaymentAgreementUpload(self):
        connstr = self.dict_data["查询条件1"]
        cmmstr = self.dict_data["输入值1"]
        reslutstr = self.comm.oracle_opt(connstr,cmmstr)
#        self.comm.write_file(reslutstr,self.row,self.comm.get_key_cell_col("执行结果"))
        updatestr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.actdb.casetitle_cn['执行结果'], reslutstr, self.dict_data['test_id'])
        self.actdb.testCaseUpdate(updatestr)

    def tearDown(self):
        #self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

