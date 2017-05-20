#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging,os, sys, types, json,random
import MySQLdb
import MySQLdb.cursors
from logger import Logger
from Utils.lyFunction import PubFunction
reload(sys)
sys.setdefaultencoding('utf8')

class TestMySqlAct(object):
    testcaseSelSql = '''select * from testcase ORDER BY test_order ASC'''  # WHERE is_run = 1
    testcase_copySelSql = '''select * from webuicase '''
    scriptcaseSelSql = '''select * from scriptcase ORDER BY test_order ASC'''  # WHERE is_run = 1

    caseselstr = '''select test_id, /*唯一标识id    列0*/
                    test_order,   /*测试执行顺序  列1*/
                    case_num,     /*用例编号      列2*/
                    is_run,       /*是否执行测试  列3*/
                    act_type,     /*操作类型      列4*/
                    act_object,   /*操作对象      列5*/
                    case_title,   /*案例名称      列6*/
                    case_details, /*案例详情      列7*/
                    test_time,    /*执行时间      列8*/
                    expected_result, /*预期结果   列9*/
                    test_result,  /*执行结果      列10*/
                    check_result, /*验证结果      列11*/
                    environment, /*环境  新增 列?*/
                    subsystem,  /*子系统  新增 列?*/
                    login_url,    /*登录地址      列12*/
                    login_user,   /*登录用户名    列13*/
                    login_pwd,    /*登录密码      列14*/
                    top_navi_menu1, /*一级菜单（顶部导航菜单） 列15*/
                    top_navi_menu2, /*二级菜单    列16*/
                    top_navi_menu3, /*三级菜单    列17*/
                    query_term1,    /*查询条件1-7 列18-24*/
                    query_term2,query_term3,query_term4,query_term5,query_term6,query_term7,
                    input_value1,   /*输入值1-40  列25-64*/
                    input_value2,input_value3,input_value4,input_value5,input_value6,input_value7,
                    input_value8,input_value9,input_value10,input_value11,input_value12,input_value13,
                    input_value14,input_value15,input_value16,input_value17,input_value18,input_value19,
                    input_value20,input_value21,input_value22,input_value23,input_value24,input_value25,
                    input_value26,input_value27,input_value28,input_value29,input_value30,input_value31,
                    input_value32,input_value33,input_value34,input_value35,input_value36,input_value37,
                    input_value38,input_value39,input_value40,
                    pri_key_index,  /*主键索引    列65*/
                    pri_key_remark  /*主键备注    列66*/
                from webuiruntime
                ORDER BY test_order ASC''' #  WHERE is_run = 1
    # 标题名称和列对应关系
    casetitle_cn = None
    table = None

    def __init__(self, host = '10.18.12.198', db = 'autotest', user = 'root', passwd = '111111', port = 3306, charset='utf8'):
        self.host = host
        self.db = db
        self.user = user
        self.passwd = passwd
        self.port = port
        self.charset = charset
        s = os.sep
        self.logstu = Logger(sys.path[0] + s + 'logs' + s + 'autotest.log', logging.DEBUG, logging.DEBUG)
        #self.logstu = Logger('autotest.log', logging.DEBUG, logging.DEBUG)
        self.casetitle_cn = self.cn_title_WebUICase()
        self.pubf = PubFunction()

    # 查询数据库，参数为sql语句，返回查询的结果，结果为二维数组以便保存多行多列结果
    def testCaseSel(self, selSql= 'SELECT VERSION()'):
        self.logstu.debug("MYSQL Select Sql：%r" % selSql)
        # 打开数据库连接
        db = MySQLdb.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset = self.charset,cursorclass = MySQLdb.cursors.DictCursor)
        cursor = db.cursor() # 使用cursor()方法获取操作游标
        rulstr = None
        try:
            cursor.execute(selSql) # 执行SQL语句
            rulstr = cursor.fetchall() # 获取所有记录列表
            #self.logstu.debug('MYSQL Select rulest: %r' % rulstr) # 打印结果
            self.logstu.debug(rulstr)
        except Exception as e:
            self.logstu.debug(e)
        db.close() # 关闭数据库连接
        return rulstr

    # 使用事务执行删除操作，失败了可以回滚，建议不用这个方法它会彻底删除数据，应用标志位表示删除
    def testCaseDel(self, delSql):
        self.logstu.debug("MYSQL Delete Sql：%s" % delSql)
        db = MySQLdb.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db ,charset = self.charset)
        cursor = db.cursor()
        n = 0
        try:
            n = cursor.execute(delSql)
            db.commit()
        except Exception as e:
            self.logstu.debug(e)
            db.rollback()
        db.close()
        self.logstu.debug('MYSQL Delete rulest: %d' % n)
        return n

    # 更新操作
    def testCaseUpdate(self, updateSql):
        self.logstu.debug("MYSQL Update Sql：%s" % updateSql)
        db = MySQLdb.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset = self.charset)
        cursor = db.cursor()
        n = 0
        try:
            n = cursor.execute(updateSql)
            db.commit()
        except Exception as e:
            self.logstu.debug(e)
            db.rollback()
        db.close()
        self.logstu.debug('MYSQL Update rulest: %d' % n)
        return n

    # 返回数据库webuicase表标题的中文字典
    def cn_title_WebUICase(self):
        dict_row_data = {
            "test_id": 'test_id',
            "执行顺序": 'test_order',
            "案例编号": 'case_num',
            "是否执行": 'is_run',
            "操作类型": 'act_type',
            "操作对象": 'act_object',
            "案例名称": 'case_title',
            "案例详情": 'case_details',
            "执行时间": 'test_time',
            "预期结果": 'expected_result',
            "执行结果": 'test_result',
            "验证结果": 'check_result',
            "环境": 'environment',
            "子系统": 'subsystem',
            "登录地址": 'login_url',
            "登录用户": 'login_user',
            "登录密码": 'login_pwd',
            "一级菜单": 'top_navi_menu1',
            "二级菜单": 'top_navi_menu2',
            "三级菜单": 'top_navi_menu3',
            "主键索引": 'pri_key_index',
            "主键备注": 'pri_key_remark'
        }
        for ii in range(1, 8):
            selstr = '查询条件' + str(ii)
            dict_row_data[selstr] = 'query_term' + str(ii)
        for ii in range(1, 41):
            valstr = '输入值' + str(ii)
            dict_row_data[valstr] = 'input_value' + str(ii)
        return dict_row_data

    def rowdata_update(self, dict_row_data, row_in):
        # 取有特殊标志的做处理
        self.logstu.debug(dict_row_data)
        for k in dict_row_data:
            findstr = self.pubf.all_type_to_encode(dict_row_data[k])
            if type(findstr) != types.StringType:
                continue
            if ('(rd' in findstr) or ('(up' in findstr) or ('(char' in findstr) or ('(time' in findstr):
                dict_row_data[k] = self.set_cell_special_value(dict_row_data[k], row_in)
                self.logstu.debug(dict_row_data[k])
                upstr = "UPDATE webuiruntime SET %s = '%s' WHERE test_id = '%s'" \
                        % (self.casetitle_cn[k], dict_row_data[k], self.table[row_in]['test_id'])
                self.logstu.debug('更新数据库：%s' % upstr)
                self.testCaseUpdate(upstr) # 更新数据库中的数据，将特定关键字如up rd替换为实际测试数据
                self.table[row_in][self.casetitle_cn[k]] = dict_row_data[k] # 对应更新内存中的数据
        return dict_row_data
    # 针对表格里各字段值的特殊处理, 参数str_in：单元格内容， row_in：行数，colname：db表列名
    def set_cell_special_value(self, str_in, row_in):
        col_in = 0
        newstr = ""
        str_in = self.pubf.all_type_to_encode(str_in)
        str_in = str_in.split("|")
        for i in range(len(str_in)):
            # 取随机数
            if '(rd' in str_in[i]:
                tp1_rd = str_in[i].split(")")
                rdnum = ""
                rdlaststr = ""
                if len(tp1_rd[0]) < 4:
                    self.logstu.debug("你当前没有指定随机数位数  -->>  请在案例里指定")
                    continue
                else:
                    tp2_rd = tp1_rd[0].split("(")
                    tp_rd_bit = int(tp2_rd[1][2:])
                    tp_rd_max = 10 ** tp_rd_bit
                    rdnum = self.pubf.all_type_to_encode((tp2_rd[0]) + str(random.randint(0, tp_rd_max)).zfill(tp_rd_bit))
                if len(tp1_rd) == 2:
                    rdlaststr = self.pubf.all_type_to_encode(tp1_rd[1])
                    rdlaststr = rdlaststr.replace("$", "")
                str_in[i] = rdnum + rdlaststr
            if '(char' in str_in[i]:
                chars = ""
                tp1_rd = str_in[i].split(")")
                tp2_rd = tp1_rd[0].split("(")
                tp_rd_bit = int(tp2_rd[1][4:])
                for j in range(tp_rd_bit):
                    chars = chars + self.pubf.GB2312()
                str_in[i] = chars
            if '(up' in str_in[i]:
                tp1_upsd = str_in[i].split(")")
                if len(tp1_upsd) == 1:
                    self.logstu.debug( "你当前没有指定取向上哪一行的的标签少')'  -->>  请在案例里修改")
                    continue
                if len(tp1_upsd[0]) < 4:
                    self.logstu.debug( "你当前没有指定取向上哪一行的数据  -->>  请在案例里指定(eg:本案例是:0行,上一条案例是:1行)")
                    continue
                if len(tp1_upsd) == 2:
                    tplast = tp1_upsd[1].split("$") # (up1)执行结果$
                    laststr = ""
                    if len(tplast) == 2:
                        tp1_upsd[1] = tplast[0]
                        laststr = self.pubf.all_type_to_encode(tplast[1])
                    # 取向上取的行数
                    tp1_upsd2 = tp1_upsd[0].split("(")
                    tp1_upsd_bit = int(tp1_upsd2[1][2:])
                    upsd_row = row_in - tp1_upsd_bit
                    # 取向上取的列名
                    selstr = "select %s from webuiruntime where test_id = '%s'" \
                             % (self.casetitle_cn[tp1_upsd[1]], self.table[upsd_row]['test_id'])
                    upsd_value = self.testCaseSel(selstr)
                    tp1_upsd2[0] = self.pubf.all_type_to_encode(tp1_upsd2[0])
                    upsd_value = self.pubf.all_type_to_encode(upsd_value[0][self.casetitle_cn[tp1_upsd[1]]])
                    if upsd_value == None:
                        upsd_value = ''
                    if type(upsd_value) != types.StringType:
                        self.logstu.debug('db查询结果不是String类型：%r' % upsd_value)
                        upsd_value = str(upsd_value)
                    new_str = tp1_upsd2[0] + upsd_value + laststr
                    self.logstu.debug('替换关键字指定内容：%s ==> %s' % (str_in[i], new_str))
                    str_in[i] = new_str
            if "(time" in str_in[i]:
                import time,datetime
                tp1 = str_in[i].split(")")
                tp2 = tp1[0].split("_")
                if tp2[1] == "today":
                    t = time.strftime("%Y/%m/%d")
                if tp2[1] == "today+1year":
                    t1 = datetime.datetime.now()
                    year = t1.year+1
                    month = t1.month
                    day = t1.day
                    if len(str(month)) == 1:
                        month = '0'+str(month)
                    if len(str(day)) == 1:
                        day = '0' + str(day)
                    t = "%s/%s/%s" %(str(year),str(month),str(day))
                tp1[0] = t
                str_in[i] = "".join(tp1)
        for j in range(len(str_in)):
            if j == len(str_in) - 1:
                newstr = self.pubf.all_type_to_encode(newstr) + str_in[j]
            else:
                newstr = self.pubf.all_type_to_encode(newstr) + self.pubf.all_type_to_encode(str_in[j]) + "|"
        return newstr

    def insertRecord(self, i):
        print i
        strInsertSql = '''insert into webuicase
            (test_id,test_order,case_num,is_run,act_type,act_object,case_title,case_details,expected_result,test_result,check_result,environment,subsystem,login_url,login_user,login_pwd, top_navi_menu1,top_navi_menu2,top_navi_menu3,query_term1,query_term2,query_term3,query_term4,query_term5,query_term6,query_term7,input_value1,input_value2,input_value3,input_value4,input_value5,input_value6,input_value7,input_value8,input_value9,input_value10,input_value11,input_value12,input_value13,input_value14,input_value15,input_value16,input_value17,input_value18,input_value19,input_value20,input_value21,input_value22,input_value23,input_value24,input_value25,input_value26,input_value27,input_value28,input_value29,input_value30,input_value31,input_value32,input_value33,input_value34,input_value35,input_value36,input_value37,input_value38,input_value39,input_value40,spare1,spare2)
            value("''' + str(self.table[i]['test_id']) + '''",
              "''' + str(self.table[i]['test_order']) + '''",
              "''' + str(self.table[i]['case_num']) + '''",
              "''' + str(self.table[i]['is_run']) + '''",
              "''' + str(self.table[i]['act_type']) + '''",
              "''' + str(self.table[i]['act_object']) + '''",
              "''' + str(self.table[i]['case_title']) + '''",
              "''' + str(self.table[i]['case_details']) + '''",
              "''' + str(self.table[i]['expected_result']) + '''",
              "",
              "",
             "''' + str(self.table[i]['environment']) + '''",
             "''' + str(self.table[i]['subsystem']) + '''",
             "''' + str(self.table[i]['login_url']) + '''",
             "''' + str(self.table[i]['login_user']) + '''",
             "''' + str(self.table[i]['login_pwd']) + '''",
             "''' + str(self.table[i]['top_navi_menu1']) + '''",
             "''' + str(self.table[i]['top_navi_menu2']) + '''",
             "''' + str(self.table[i]['top_navi_menu3']) + '''",
             "''' + str(self.table[i]['query_term1']) + '''",
             "''' + str(self.table[i]['query_term2']) + '''",
             "''' + str(self.table[i]['query_term3']) + '''",
             "''' + str(self.table[i]['query_term4']) + '''",
             "''' + str(self.table[i]['query_term5']) + '''",
             "''' + str(self.table[i]['query_term6']) + '''",
             "",
             "''' + str(self.table[i]['input_value1']) + '''",
             "''' + str(self.table[i]['input_value2']) + '''",
             "''' + str(self.table[i]['input_value3']) + '''",
             "''' + str(self.table[i]['input_value4']) + '''",
             "''' + str(self.table[i]['input_value5']) + '''",
             "''' + str(self.table[i]['input_value6']) + '''",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "",
             "''' + str(self.table[i]['spare1']) + '''",
             "''' + str(self.table[i]['spare2']) + '''"
             )'''
        self.testCaseUpdate(strInsertSql)
        # print strInsertSql

    def UpdateCaseRecord(self, i):
        strUpdateSql = '''update webuicase set
          test_order ="''' + str(self.table[i]['test_order']) + '''",
          case_num ="''' + str(self.table[i]['case_num']) + '''",
          is_run ="''' + str(self.table[i]['is_run']) + '''",
          act_type ="''' + str(self.table[i]['act_type']) + '''",
          act_object ="''' + str(self.table[i]['act_object']) + '''",
          case_title ="''' + str(self.table[i]['case_title']) + '''",
          case_details ="''' + str(self.table[i]['case_details']) + '''",
          expected_result ="''' + str(self.table[i]['expected_result']) + '''",
          environment ="''' + str(self.table[i]['environment']) + '''",
          subsystem ="''' + str(self.table[i]['subsystem']) + '''",
          login_url ="''' + str(self.table[i]['login_url']) + '''",
          login_user ="''' + str(self.table[i]['login_user']) + '''",
          login_pwd ="''' + str(self.table[i]['login_pwd']) + '''",
          top_navi_menu1 ="''' + str(self.table[i]['top_navi_menu1']) + '''",
          top_navi_menu2 ="''' + str(self.table[i]['top_navi_menu2']) + '''",
          top_navi_menu3 ="''' + str(self.table[i]['top_navi_menu3']) + '''",
          query_term1 ="''' + str(self.table[i]['query_term1']) + '''",
          query_term2 ="''' + str(self.table[i]['query_term2']) + '''",
          query_term3 ="''' + str(self.table[i]['query_term3']) + '''",
          query_term4 ="''' + str(self.table[i]['query_term4']) + '''",
          query_term5 ="''' + str(self.table[i]['query_term5']) + '''",
          query_term6 ="''' + str(self.table[i]['query_term6']) + '''",
          input_value1 ="''' + str(self.table[i]['input_value1']) + '''",
          input_value2 ="''' + str(self.table[i]['input_value2']) + '''",
          input_value3 ="''' + str(self.table[i]['input_value3']) + '''",
          input_value4 ="''' + str(self.table[i]['input_value4']) + '''",
          input_value5 ="''' + str(self.table[i]['input_value5']) + '''",
          input_value6 ="''' + str(self.table[i]['input_value6']) + '''",
          spare1 ="''' + str(self.table[i]['spare1']) + '''",
          spare2 ="''' + str(self.table[i]['spare2']) + '''"
          where test_id = "''' + str(self.table[i]['test_id']) + '''"'''
        self.testCaseUpdate(strUpdateSql)
        print strUpdateSql


if __name__ =='__main__':
    actdb = TestMySqlAct(host = '10.20.2.90', db = 'chrs_autotest', user = 'root', passwd = '111111', port = 3306, charset='utf8')

    actdb.testCaseUpdate("update interface set case_id = 223221 where interface_order = 10000100")
    aastr = actdb.testCaseSel("select case_id from interface  where interface_order = 10000100")
    print aastr
    '''
    #actdb.testCaseDel('TRUNCATE webuiruntime')  # 删除临时表数据
    # copy 需要执行的测试用例到临时表
    #actdb.testCaseUpdate('INSERT INTO webuiruntime SELECT * FROM webuicase WHERE webuicase.is_run = 1')
    #actdb.table = actdb.testCaseSel(actdb.caseselstr)
    #print actdb.testCaseSel()
    print actdb.testCaseSel("select input_value12 from webuicase;")

    #table = actdb.testCaseSel(selSql = 'select test_id, test_order, case_num, is_run from webuiruntime ORDER BY test_order ASC')
    #table = actdb.testCaseSel(selSql='select test_id, test_order, case_num, is_run from webuiruntime ORDER BY test_order desc')
    print 'select:\n',actdb.table
    print len(actdb.table)
    if actdb.table[1]['input_value35'] == None:
        print 'haha None'
    if actdb.table[1]['input_value35'] == '':
        print 'haha null'
    '''