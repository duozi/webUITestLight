# -*- coding: UTF-8 -*-
import sys, os

class I_TXT_Act(object):
    def read_stata_txt(self,filename):
        if os.path.exists(filename) == False:
            return 'no find file' + filename
        file_object = open(filename)
        try:
            all_the_text = file_object.read()
            print all_the_text
        finally:
            file_object.close()
        return all_the_text
    def write_stat_txt(self,filename, datatxt):
        file_object = open(filename, 'w')
        try:
            file_object.write(datatxt)
        finally:
            file_object.close()

    # 替换文件内容
    def modifyip(self,tfile,sstr,rstr):
        try:
            lines=open(tfile,'r').readlines()
            flen=len(lines)-1
            for i in range(flen):
                if sstr in lines[i]:
                    lines[i]=lines[i].replace(sstr,rstr)
            open(tfile,'w').writelines(lines)
        except Exception as e:
            print(e)

    # 批量替换某目录下文件内容，不含子目录
    def piliang_modifyip(self, fpath, sstr, rstr):
        if os.path.exists(fpath) == False:
            print "not exists"
            return
        if os.path.isdir(fpath) == False:
            print "not a dir"
            return
        for dir_path, subpaths, files in os.walk(fpath, False):
            for file in files:
                file_path = os.path.join(dir_path, file)
                print "file:%s" % file_path
                self.modifyip(file_path, sstr, rstr)

if __name__ == '__main__':
    s = os.sep
    xmlpath = sys.path[0] + s + 'output'
    wr = I_TXT_Act()
    wr.piliang_modifyip(xmlpath,  'encoding="UTF-8"?>','encoding="UTF-8"?> ')

