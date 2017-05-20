#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging,os, sys, types, json,random,cx_Oracle
from logger import Logger
from Utils.LYPubFunction import LYPubFunction
reload(sys)
sys.setdefaultencoding('utf8')

class OracleAct(object):
    def __init__(self, host = '10.18.12.198', db = 'autotest', user = 'root', passwd = '111111', port = 3306, charset='utf8'):
        self.host = host
        self.db = db
        self.user = user
        self.passwd = passwd
        self.port = port
        self.charset = charset
        s = os.sep
        self.logstu = Logger(sys.path[0] + s + 'logs' + s + 'autotest.log', logging.DEBUG, logging.DEBUG)

    # 数据库操作,查询oracle数据库，注意参数绑定方法sql中 :1 :2 为占位符，且不能用引号引起来
    # 对应的参数和占位符对应，参数为列表[] ，元素的个数与占位符相等否则会报异常
    def oracle_act(self, ora_conn, ora_sql, ora_params=[]):
        conn = cx_Oracle.connect(ora_conn)
        cursor = conn.cursor()
        cursor.execute(ora_sql, ora_params)
        conn_res_str = cursor.fetchall()
        self.logstu.info("sql执行的结果是: %s" % (conn_res_str))
        if len(conn_res_str) == 0:
            conn_res_str = [('',)]
        alltmp = ''
        alltmp_list = []
        for tmp in conn_res_str:
            alltmp_list.append(str(tmp[0]))  # 将元组列表转为列表
            if alltmp == '':
                alltmp = str(tmp[0])
            else:
                alltmp = alltmp + ' | ' + str(tmp[0])
        self.logstu.info("sql执行的结果是: %s" % (alltmp))
        self.logstu.info("结果 1 是: %s" % (conn_res_str[0][0]))
        conn.commit()
        cursor.close()
        conn.close()
        return alltmp_list

if __name__ =='__main__':
    test = OracleAct()
    ora_conn = 'clbs/clbs#123456@10.18.12.41:1521/xiaoniu'
    ora_sql = 'SELECT t.NAME_ FROM  clbs.FIL_PROJECT_HEAD H, clbs.JBPM4_TASK T WHERE H.JBPM_ID =t.execution_id_ AND H.ID=:1'
    #ora_sql = 'SELECT t.NAME_,H.ID FROM  clbs.FIL_PROJECT_HEAD H, clbs.JBPM4_TASK T WHERE H.JBPM_ID =t.execution_id_'
    haha = test.oracle_act(ora_conn, ora_sql, ['570765'])  #
    print haha, haha[0].decode('gbk')

    ora_conn = 'clbs_dev/CLbs(123)@58.251.73.211:31579/xiaoniu'
    # ora_sql = 'SELECT H.ID PROJECT_ID FROM clbs.FIL_PROJECT_HEAD H, clbs.FIL_RENT_PLAN_HEAD FRPH,clbs.FIL_PROJECT_EQUIPMENT FPE WHERE H.ID = FRPH.PROJECT_ID AND H.ID = FPE.PROJECT_ID AND H.STATUS = 20'
    ora_sql = 'SELECT t.NAME_ FROM  clbs_dev.FIL_PROJECT_HEAD H, clbs_dev.JBPM4_TASK T WHERE H.JBPM_ID =t.execution_id_'
    haha = test.oracle_act(ora_conn, ora_sql, '')