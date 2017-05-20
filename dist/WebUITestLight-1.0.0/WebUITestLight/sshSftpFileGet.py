#!/usr/bin/python
# -*- coding: UTF-8 -*-
import paramiko, os, stat

class ISftpFileAct(object):
    ftp_server   = "10.18.12.198"
    ftp_port     = 22
    ftp_user     = "selenium"
    ftp_password = "zaq12wsx"
    # 上传文件
    def sftp_stor_files(self,file_zip, destFile):
        t = paramiko.Transport((self.ftp_server, self.ftp_port))
        t.connect(username=self.ftp_user, password=self.ftp_password, hostkey=None)
        sftp = paramiko.SFTPClient.from_transport(t)
        # dirlist on remote host, 列出远程sftp服务器上文件或文件夹列表
        dirlist = sftp.listdir('.')
        print "Dirlist:", dirlist
        sftp.put(file_zip, destFile)
        t.close()

    # 下载文件
    def sftp_down_files(self, sftpFile, localFile):
        t = paramiko.Transport((self.ftp_server, self.ftp_port))
        try:
            t.connect(username=self.ftp_user, password=self.ftp_password, hostkey=None)
            sftp = paramiko.SFTPClient.from_transport(t)
            # dirlist on remote host, 列出远程sftp服务器上文件或文件夹列表
            #dirlist = sftp.listdir('.')
            #print "Dirlist:", dirlist
            sftp.get(sftpFile,localFile)
        except Exception as e:
            print e
        finally:
            t.close()

    # 批量下载文件
    def sftp_down_dir(self, remote_dir, local_dir):
        # 去掉路径字符串最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]
        if local_dir[-1] == '/':
            local_dir = local_dir[0:-1]
        # 判断下载的目录在本地是否存在，不存在就创建
        try:
            if os.path.exists(local_dir) == False:
                os.makedirs(local_dir)
        except Exception as e:
            print e
        # 保存所有文件的列表
        all_files = list()

        t = paramiko.Transport((self.ftp_server, self.ftp_port))
        t.connect(username=self.ftp_user, password=self.ftp_password, hostkey=None)
        sftp = paramiko.SFTPClient.from_transport(t)

        # dirlist on remote host, 列出远程sftp服务器上文件或文件夹列表
        dirlist = sftp.listdir(remote_dir)
        # listdir_attr 获取当前指定目录下的所有目录及文件，包含属性值
        attrlist = sftp.listdir_attr(remote_dir)
        print "Dirlist:", dirlist
        print "Attrlist:", attrlist
        for f in attrlist:
            # remote_dir目录中每一个文件或目录的完整路径
            filename =  remote_dir + '/' + f.filename  #os.path.join(remote_dir, f)
            # 拼装本地完整路径
            localfilename = local_dir + '/' + f.filename  # os.path.join(remote_dir, f)
            print filename
            # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
            if stat.S_ISDIR(f.st_mode):
                all_files.extend(self.sftp_down_dir(filename, localfilename))
            else:
                # 是文件则下载
                sftp.get(filename, localfilename)
                all_files.append(filename)
        t.close()
        return all_files
    def sftp_file_list(self, sftpPath):
        t = paramiko.Transport((self.ftp_server, self.ftp_port))
        t.connect(username=self.ftp_user, password=self.ftp_password, hostkey=None)
        sftp = paramiko.SFTPClient.from_transport(t)
        # dirlist on remote host, 列出远程sftp服务器上文件或文件夹列表
        dirlist = sftp.listdir(sftpPath) #sftpPath
        attrlist = sftp.listdir_attr(sftpPath)
        print "Dirlist:", dirlist
        print "Listdir_attr:", attrlist
        t.close()
        return dirlist

    def ssh2_exec_command(self, command):
        print "ssh2 execute command: %s" % (command)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ftp_server, username=self.ftp_user, password=self.ftp_password)
        stdin, stdout, stderr = ssh.exec_command(command)
        stdin.close()
        for line in stdout.read().splitlines():
            print line
        for line in stderr.read().splitlines():
            print "command error ---%s" % (line)

if __name__ == '__main__':
    isftp = ISftpFileAct()
    #isftp.sftp_stor_files('logger.py','test22.py')
    #isftp.sftp_down_files('test22.py','121213.py')
    #print isftp.sftp_file_list('.')
    #print isftp.sftp_file_list('/auto_test/cbs_autotest/output')
    #isftp.ssh2_exec_command('date')
    filelist = isftp.sftp_file_list('auto_test/WebUITestLight/output')

    print isftp.sftp_down_dir('auto_test/WebUITestLight/output', 'output/')
    print 'Down File End!'
    #for file in filelist:
        #isftp.sftp_down_files('/auto_test/cbs_autotest/output/' + file, 'output/' + file)
