#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, time
reload(sys)
sys.setdefaultencoding('utf8')

class CustTestRult(object):
    errors = []
    successes = []
    failures = []
    skipped = []

    def __init__(self):
        self.errors.append([CustError(),''])
        self.start_time = time.time()
        self.stop_time = time.time()

class CustError(object):
    test_id = ''
    test_description=''
    test_exception_info=''
    test_result = None
    def __init__(self):
        self.test_result = I_test_result()
class I_test_result(object):
    _stdout_data  = ''


if __name__ == '__main__':
    var = CustTestRult()
    print var.errors[0][0].test_id
    print var.errors[0][1]