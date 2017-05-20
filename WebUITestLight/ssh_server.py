#!/usr/bin/env python
#coding:GBK

import SocketServer,os,time,sys
from datetime import datetime
#import logbak

class petServer(SocketServer.BaseRequestHandler):
    def handle(self):
        print "Got Connection from :%s at %s" %(self.client_address[0],datetime.now())
        while 1:
            self.data=self.request.recv(4096).strip()
            #logbak.logger(self.client_address[0],self.data)
            if not self.data:continue
            if self.data == "exit" or self.data == "quit":break
            #GET FILE
            if self.data.split()[0] == "get":
                try:
                    f_name = self.data.split()[1]
                    f = open(f_name,'rb')
                    f_data = f.read()
                    f.close()
                    self.request.sendall(f_data)
                    time.sleep(1)
                    self.request.send("done")
                except Exception,e:
                    return e
                continue
            #RENAME FILE
            elif self.data.split()[0] == "mv":
                try:
                    f_name_old = self.data.split()[1]
                    f_name_new = "%s_%s" %(self.data.split()[1], time.strftime('%Y%m%d%H%M%S'))
                    os.rename(f_name_old, f_name_new)
                except Exception,e:
                    return e
                self.request.sendall("Done")
                continue
            elif self.data.split()[0] == "rm":
                try:
                    f_name = self.data.split()[1]
                    os.remove(f_name)
                except Exception,e:
                    return e
                self.request.sendall("Done")
                continue
            elif self.data.split()[0] == "jar":
                try:
                    d_name_old = self.data.split()[1]
                    #d_name_new = "%s_%s.jar" %(self.data.split()[1], time.strftime('%Y%m%d%H%M%S'))
                    d_name_new = "%s.jar" % self.data.split()[1]
                    os.popen('jar cfM %s %s' %(d_name_new, d_name_old))
                except Exception,e:
                    return e
                self.request.sendall("Done")
                continue
            else:
                try:
                    os.chdir(r"C:\auto_test\WebUITestLight")
                    cmd_results = os.popen(self.data).read()
                except Exception,e:
                    return e
                #print cmd_results
                self.request.sendall(cmd_results)
        

if __name__ == "__main__":
    host,port = '',22
    print "Server Started ..."
    S = SocketServer.ThreadingTCPServer((host,port),petServer)
    S.serve_forever()
