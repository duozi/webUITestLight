#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging,os, sys, types, json,random
import MySQLdb
import MySQLdb.cursors
from logger import Logger
reload(sys)
sys.setdefaultencoding('utf8')

class MySqlAct(object):

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


if __name__ =='__main__':
    actdb = MySqlAct(host = '127.0.0.1', db = 'chrs_autotest', user = 'root', passwd = '111111', port = 3306, charset='utf8')
    aastr = actdb.testCaseSel("select case_id from interface")
    print aastr