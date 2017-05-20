#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, subprocess, time
import socket               # 导入 socket 模块
import reWriteXml

def work():
    s = socket.socket()         # 创建 socket 对象
    host =  '10.20.2.90'# socket.gethostname()获取本地主机名 :'XJ-LP-00366'
    port = 12347                # 设置端口
    print (host, port)
    s.bind((host, port))        # 绑定端口

    s.listen(5)                 # 等待客户端连接
    while True:
        try:
            conn, addr = s.accept()     # 建立客户端连接。
            print '连接地址：', addr
            ret = conn.recv(2048)

            result = os.popen(ret).read()
            conn.send(result)
            conn.close()                # 关闭连接
        except Exception as e:
            print 'Exception:',e
def run_shell_and_show_reult(command, code = 'utf-8'):
    print '-------------',command, '-------------'
    result = subprocess.Popen(command,
                              # stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
    while True:
        data = result.stdout.readline()
        if not data:
            break
        print data.decode(encoding=code)
    print ''

if __name__ == '__main__':
    s = os.sep
    wr = reWriteXml.I_TXT_Act()
    wr.write_stat_txt('TestState','End')
    while True:
        txt = wr.read_stata_txt('TestState')
        if txt == 'End':
            time.sleep(3)
        if txt.find('Start') > -1:
            print 'Start WebUITest Test'
            timeStr = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            movelog = 'move logs'+s+'autotest.log logs'+s+timeStr + '.log'
            print movelog
            wr.write_stat_txt('TestState', 'Continue')

            run_shell_and_show_reult(movelog, 'gbk')
            run_shell_and_show_reult('svn update', 'gbk')
            wr.write_stat_txt('TestState', 'Continue')
            #run_shell_and_show_reult('python main.py')
            # 拼装启动命令，增加了启动参数，判断测试环境和系统
            txt = txt.replace('Start', 'python main_Script.py')
            print subprocess.check_output(txt, shell=True).decode(encoding='utf-8')
            time.sleep(3)
            wr.write_stat_txt('TestState', 'End')
        time.sleep(1)
