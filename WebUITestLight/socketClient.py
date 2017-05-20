#!/usr/bin/python
# -*- coding: UTF-8 -*-
import paramiko, os, stat,sys
import datetime
import time
import socket               # 导入 socket 模块
import reWriteXml
import sshSftpFileGet

def socket_send(command):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('10.18.12.198', 12347))
        sock.send(command)
        result = sock.recv(2048)
        sock.close()
        return result

if __name__ == '__main__':
    sonSys = 'All'
    testENV = 'All'  # 环境默认值 uat， 还有stg等
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            print "Start Parameter:", i, sys.argv[i]
            if sys.argv[i].find("=") != -1:
                tmp = sys.argv[i].split('=')
                if tmp[0].upper() == 'S' or tmp[0].upper() == 'SYS':
                    sonSys = tmp[1]
                if tmp[0].upper() == 'V' or tmp[0].upper() == 'ENV':
                    testENV = tmp[1]
            else:
                testENV = sys.argv[1]
                if i == 2:
                    sonSys = sys.argv[2]

    ifalg = True
    sshclass = sshSftpFileGet.ISftpFileAct()
    wr = reWriteXml.I_TXT_Act()
    wr.write_stat_txt('TestState', 'Start' + ' v=' + testENV + ' s=' + sonSys)
    time1 = time.time()
    while True:
        if time.time() - time1 > 25560: # 超过半小时 60分钟=3600秒 自动退出
            print u'执行测试等待结果超过了7.1小时，请检查执行机上服务是否启动'
            break
        txt = wr.read_stata_txt('TestState')
        if txt == 'End':
            print 'Test End!'
            break
        if txt.find('Start') > -1:
            if ifalg:
                sshclass.sftp_stor_files('TestState', 'AutoTest/WebUITestLight/TestState')
                ifalg = False
            print 'Start UITest!'
            for i in range(0, 30):
                time.sleep(10)
                sshclass.sftp_down_files('AutoTest/WebUITestLight/TestState', 'TestState')
                txt = wr.read_stata_txt('TestState')
                if txt != 'Start':
                    break
        if txt == 'Continue':
            try:
                sshclass.sftp_down_files('AutoTest/WebUITestLight/TestState', 'TestState')
            except Exception as e:
                print 'Client:', e
            print 'Continue'
            time.sleep(30)

    isftp = sshSftpFileGet.ISftpFileAct()
    filelist = isftp.sftp_file_list('AutoTest/WebUITestLight/output')
    print isftp.sftp_down_dir('AutoTest/WebUITestLight/output', 'output/')
    print 'Down File End!'

    s = os.sep
    xmlpath = sys.path[0] + s + 'output'
    wr.piliang_modifyip(xmlpath, 'encoding="UTF-8"?>', 'encoding="UTF-8"?> ')

    print ''
    print '======== Console Report ======='
    wr.read_stata_txt(xmlpath + s + 'Report.txt')
    print ''

