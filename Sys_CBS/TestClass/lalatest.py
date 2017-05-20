#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
from script.testunite.comm.lyElementsOperation import PublicAct

class Lalatest(unittest.TestCase):
    '''系统管理>用户管理'''
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象


    def setUp(self):
        self.driver = self.mainWebDr
        self.pub = PublicAct(self.driver)
        self.pub.logstu.debug('test1 setUp')

    # 测试类
    def test_1(self):
        self.pub.logstu.debug('test1 test')


