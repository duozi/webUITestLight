#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging,os, sys, types, json,random
import MySQLdb
import MySQLdb.cursors
from logger import Logger
reload(sys)
sys.setdefaultencoding('utf8')

class MySqlAct_zsh(object):
    testcaseSelSql = '''select * from testcase ORDER BY test_order ASC'''  # WHERE is_run = 1
    testcase_copySelSql = '''select * from testcase_copy '''

    # 标题名称和列对应关系

    def __init__(self, host = '10.18.12.198', db = 'autotest', user = 'root', passwd = '111111', port = 3306, charset='utf8'):
        self.host = host
        self.db = db
        self.user = user
        self.passwd = passwd
        self.port = port
        self.charset = charset
        s = os.sep
        self.logstu = Logger(sys.path[0] + s + 'logs' + s + 'autotest.log', logging.DEBUG, logging.DEBUG)

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

    # 更新操作,防注入
    def testCaseUpdate2(self, updateSql, *params):
        self.logstu.debug("MYSQL Update Sql：%s" % updateSql)
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                             charset=self.charset)
        cursor = db.cursor()
        n = 0
        try:
            n = cursor.execute(updateSql, params)
            db.commit()
        except Exception as e:
            self.logstu.debug(e)
            db.rollback()
        db.close()
        self.logstu.debug('MYSQL Update rulest: %d' % n)
        return n

    def insertRecord(self,i):
        print i
        strInsertSql = '''insert into testcase_copy
            (test_id,test_order,case_num,is_run,act_type,act_object,case_title,case_details,expected_result,environment,subsystem,login_url,login_user,login_pwd,top_navi_menu1,top_navi_menu2,top_navi_menu3,query_term1,query_term2,query_term3,query_term4,query_term5,query_term6,input_value1,input_value2,input_value3,input_value4,input_value5,input_value6,spare1,spare2)
            value("''' + str(self.table[i]['test_id']) + '''",
              "''' + str(self.table[i]['test_order']) + '''",
              "''' + str(self.table[i]['case_num']) + '''",
              "''' + str(self.table[i]['is_run']) + '''",
              "''' + str(self.table[i]['act_type']) + '''",
              "''' + str(self.table[i]['act_object']) + '''",
              "''' + str(self.table[i]['case_title']) + '''",
              "''' + str(self.table[i]['case_details']) + '''",
              "''' + str(self.table[i]['expected_result']) + '''",
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
             "''' + str(self.table[i]['input_value1']) + '''",
             "''' + str(self.table[i]['input_value2']) + '''",
             "''' + str(self.table[i]['input_value3']) + '''",
             "''' + str(self.table[i]['input_value4']) + '''",
             "''' + str(self.table[i]['input_value5']) + '''",
             "''' + str(self.table[i]['input_value6']) + '''",
             "''' + str(self.table[i]['spare1']) + '''",
             "''' + str(self.table[i]['spare2']) + '''"
             )'''
        self.testCaseUpdate(strInsertSql)
        # print strInsertSql
    def UpdateCaseRecord(self,i):
        strUpdateSql = '''update testcase_copy set
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
    actdb = MySqlAct_zsh(host = '127.0.0.1', db = 'chrs_autotest', user = 'root', passwd = '111111', port = 3306, charset='utf8')
    aastr = actdb.testCaseSel("select case_id from interface")
    print aastr