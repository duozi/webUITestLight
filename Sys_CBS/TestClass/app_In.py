# coding=gbk
import socket,threading,time,math,sys,signal,random,xlrd,xlwt,cx_Oracle,os,json,httplib,urllib,urllib2,errno,unittest
from xlutils.copy import copy
from xml.etree import ElementTree
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from socket import error as SocketError
reload(sys)
sys.setdefaultencoding('GBK')

class AppIn(unittest.TestCase):
    path=''
    recv_body_col = -1
    send_body_col = -1
    req_add_col = -1
    exec_type_col = -1
    req_body_col = -1
    expect_result_col = -1
    result_col = -1
    is_exec_col = -1
    is_exec_type_col = -1
    case_name_col = -1
    sys_env_col = -1
    curedate=time.strftime('%Y/%m/%d %X',time.localtime())
    sheetname = 'appin' #���ö�ȡ��sheet���
    file_name = 'data/testcase.xls'
    sheetindex= 2
    dict_data = ''  # ����main�ű��������Ĳ���
    mainWebDr = ""  # ����main�ű���������
    comm = ""  # ����main�ű����͵Ĺ�����ʵ������
    row = ""  # ����main�ű����͵ĵ�ǰ���������
    logstu = ""  # ����main�ű���������дlog�Ķ���


    #��ȡ��ǰ·��
    def cur_file_dir(self):
        path = self.path
        file_name = self.file_name
        path_tp=''
        path_tp1=''
        path_tp2 =  sys.path[0]
        if os.path.isdir(path_tp2):
            path_tp1 = path_tp2
        elif os.path.isfile(path_tp2):
            path_tp1 = os.path.dirname(path_tp2)
        path_tp = path_tp1.split('/')
        for i in range(len(path_tp)):
            path=path+str(path_tp[i])+'/'
        self.path=path+file_name
        return path

    # ��ȡ�ļ�����   ��sheet����
    def load_files(self,sheetname):           # ��ȡ�ļ�����
        #self.logstu.debug(self.path)
        #self.logstu.debug(sheetname)
        data = xlrd.open_workbook(self.path)
        table=data.sheet_by_name(sheetname)
        return table


    #��ȡ������Ӧ�ĵڼ���  �������ݣ�����
    def get_key_cell_col(self,table_in,keyname_in):
        label = 0
        ncols = table_in.ncols
        for i in range(ncols):
            strtemp2 = table_in.cell(0,i).value
            strtemp2 = strtemp2.encode("GBK")
            if keyname_in==strtemp2:
                label = 1
                return i
        if label == 0 :
            self.logstu.debug(("û��ȡ���� "+keyname_in+" ����Ӧ������"))

    # ��ȡ�ṹ���Ͷ�Ӧ������������������sheet����
    def read_comm_param(self):
        table = self.load_files(self.sheetname)
        self.recv_body_col = self.get_key_cell_col(table,'���ر���')
        self.send_body_col = self.get_key_cell_col(table,"���ͱ���")
        self.expect_result_col = self.get_key_cell_col(table,"Ԥ�ڽ��")
        self.req_add_col = self.get_key_cell_col(table,"�����ַ")
        self.result_col = self.get_key_cell_col(table,"��֤���")
        self.is_exec_col = self.get_key_cell_col(table,"�Ƿ�ִ��")
        self.exec_type_col = self.get_key_cell_col(table,"ִ�з�ʽ")
        self.req_body_col = self.get_key_cell_col(table,"������")
        self.case_name_col = self.get_key_cell_col(table,"��������")
        self.sys_env_col = self.get_key_cell_col(table,"ϵͳ����")
        self.is_exec_type_col = self.get_key_cell_col(table,"��������")
        return table

    #��ȡǰ��洢������
    def get_above_str(self,table,need_read_str_in,row_in):
        recv_body_col = self.recv_body_col
        send_body_col = self.send_body_col
        sheetname = self.sheetname
        table_in = self.load_files(sheetname)
        find_col = 0
        need_read_str = str(need_read_str_in).decode('string_escape')
        tp_str1=need_read_str.split(')')
        up_now=int(tp_str1[0][5:])   #����ȡ�������ڵڼ���
        tp_str2=tp_str1[1].split('=')
        if '(upsd' in need_read_str:
            find_col = send_body_col
        if '(uprc' in need_read_str:
            find_col = recv_body_col
        data_cell_value = table_in.cell((row_in-up_now),find_col).value
        data_cell_value = data_cell_value.replace("'",'"')
        find_str = tp_str2[1]
        keystr=tp_str2[0]
        valuestr = ''
        if (find_str in data_cell_value) :
            valuetemp1 = data_cell_value.split(find_str)
            valuetemp2 = valuetemp1[1].split('":"')
            valuetemp3 = valuetemp2[1].split('"')
            valuestr = valuetemp3[0]
        return keystr,valuestr.encode("GBK")   #���ز��ҵĹؼ���+��Ӧ��ֵ

    #��ȡ������,���ؽ����ַ+���ͱ���
    def read_request(self,table_in,row_in):
        req_body_col = self.req_body_col
        recv_body_col = self.recv_body_col
        req_add_col = self.req_add_col
        body_str=""
        body_str_comm=table_in.cell(row_in,req_body_col).value
        body_str_comm=body_str_comm.replace('"',"'")
        temp1=body_str_comm.split("'")
        for j in range(len(temp1)-1):
            if temp1[j]<>'':
                keystr=''
                valuestr=''
                if ('(up' in temp1[j]):
                    key_str,value_str = self.get_above_str(table_in,temp1[j],row_in)
                    temp1[j] = key_str+'":"'+value_str
                    temp1[j] = temp1[j].decode("GBK")
                elif ('(rd' in temp1[j]):
                    print temp1[j]
                    frststr = ""
                    laststr = ""
                    tp1 = temp1[j].split("(rd")
                    frststr = str(tp1[0])
                    tp2 = tp1[1].split(")")
                    rd_bit = tp2[0]
                    if rd_bit =="":
                        rd_bit = 12
                    tp_rd_max = 10**int(rd_bit)
                    rdnum = str(random.randint(0,tp_rd_max)).zfill(int(rd_bit))
                    if "$" in tp2[1]:
                        tp3 = tp2[1].split("$")
                        key_str = str(tp3[0])
                        laststr = str(tp3[1])
                    else:
                        key_str = str(tp2[1])

                    value_str = frststr + rdnum + laststr
                    temp1[j]=key_str+'":"'+value_str
                    print temp1[j]
                elif ('(char' in temp1[j]):
                    print temp1[j]
                    frststr = ""
                    laststr = ""
                    rdchar = ""
                    tp1 = temp1[j].split("(char")
                    frststr = str(tp1[0])
                    tp2 = tp1[1].split(")")
                    rd_bit = tp2[0]
                    print rd_bit
                    if rd_bit =="":
                        rd_bit = 3
                    for t in range(int(rd_bit)):
                        rdchar = rdchar + self.GB2312()
                    print tp2[1]
                    if "$" in tp2[1]:
                        tp3 = tp2[1].split("$")
                        key_str = str(tp3[0])
                        laststr = str(tp3[1])
                    else:
                        key_str = tp2[1]
                    value_str = frststr + rdchar + laststr
                    temp1[j]=key_str+'":"'+value_str
                    print temp1[j]
            body_str=body_str+temp1[j]+'"'
        body_str=body_str+temp1[len(temp1)-1]
        #��ȡ�����ַ
        urlstr=table_in.cell(row_in,req_add_col).value
        body_str=body_str.replace("$curedate",self.curedate)
        return urlstr,body_str

     #���ڲ����������
    def GB2312(self):
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0, 0xF)
        val = ( head << 8 ) | (body << 4) | tail
        str = "%x" % val
        restr = ""
        try:
            restr = str.decode('hex').decode('gbk')
        except UnicodeDecodeError as e:
            print e
        return restr

    # д���ݵ���Ӧ�ı����
    def write_file(self,str_in,row_in,col_in):   #д������ݡ�str_in�� һ��Ҫ�ǣ�unicode����
        path = self.path
        datas = xlrd.open_workbook(path)
        newdatas = copy(datas)
        newtable = newdatas.get_sheet(self.sheetindex)
        #data_in = unicode(str_in,"gbk")
        newtable.write(row_in,col_in,str_in)
        newdatas.save(path)
        self.logstu.debug(u'�ɹ���������:  ' + str_in)

    #ȡԤ�ڵĹؼ���
    def get_yuqi_key(self,table_in,row_in):
        expect_result_col = self.expect_result_col
        yuqi_str_temp =  table_in.cell(row_in,expect_result_col).value
        yuqi_str_temp = str(yuqi_str_temp)
        yq_str = yuqi_str_temp.split('&')
        yqstr = []
        for j in range(len(yq_str)):
            if "|" in yq_str[j]:
                yuqi_str = yq_str[j].split('|')
                for i in range(len(yuqi_str)):
                    if '(up' in yuqi_str[i]:
                        key_str,value_str = self.get_above_str(table_in ,yuqi_str[i],row_in)
                        yqstr.append(key_str+'":"'+value_str)
            else:
                yqstr.append(yq_str[j])
            self.logstu.debug(u"Ԥ�ڽ����="+str(yqstr))
        return yqstr

    #�ж�Ԥ�ڹؼ��֣��Ƿ���ڷ��صĽ���У��������PASS   ���������FAIL
    def is_pass(self,table_in,rcvstr_in,nrows_in):
        label = 0
        yq_str = self.get_yuqi_key(table_in,nrows_in)   #ȡ��Ԥ�ڵĹؼ���
        rcvstr_in = rcvstr_in.replace("'",'"')
        for i in range(len(yq_str)):
            if yq_str[i] in (unicode(rcvstr_in,"gbk")): #�����Խ����¼�������
                label = label + 1
        if label == len(yq_str):
            self.logstu.debug("pass-------------")
            self.write_file('PASS',nrows_in,self.result_col)
        else :
            self.write_file('FAIL',nrows_in,self.result_col)
            self.logstu.debug("faile================")

    #����httpPost����
    def http_post_send(self,url,data_in):
        tp1 = url.split(',')
        ip = tp1[0]   #ȡĿ���ַ
        serverstr = tp1[1]  #ȡ������
        data_in = data_in.replace('"',"'")
        tms1 = eval("("+data_in+")") # ת�����ͱ�����������Ϊdict
        params = urllib.urlencode(tms1)
        params = params.replace("5Cx","")  #���������ַ�������
        #params = urllib.urlencode({'TransMessage':{'CHNNO':'APP','TRANSDATE':'2016/04/19 13:37:13','TRANSCODE':'SR001','ARRAYDATA':[{'USERID':'6770022','PASSWORD':'6E147275FAB5BBD5F02B083274185BEE','PADID':'867279020698207'}]}})
        headers = {"Content-type": "application/x-www-form-urlencoded;charset=GBK","Accept": "text/plain"}
        #headers = {"Content-type": "application/json;charset=GBK","Accept": "text/json"}
        conn = httplib.HTTPConnection(ip)

        conn.request("POST", serverstr, params, headers)
        try:
            response = conn.getresponse()
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise #not error we are looking for
            pass # Handle error here
        #self.logstu.debug(response.status+response.reason)
        data = response.read()
        response_strs = urllib.unquote(data)
        conn.close()
        return response_strs



    #����httpPost_file����
    def http_post_file_send(self,url,data_in):
        # �� urllib2 ��ע�� http ��������
        register_openers()
        # ��ʼ���ļ� "DSC0001.jpg" �� multiart/form-data ����
        # "image1" �ǲ��������֣�һ��ͨ�� HTML �е� <input> ��ǩ�� name ��������
        # headers ��������� Content-Type �� Content-Length
        # datagen ��һ�����������󣬷��ر������Ĳ���
        datagen, headers = multipart_encode({"file": open(data_in, "rb")})
        add_headers = {"Authorization" : "Basic eGlhb25pdTpzdXBlcnNvbmlj","EncType":"multipart/form-data"}
        headers.update(add_headers)
        # �����������localhost������IP��ַ��5000�������˿ڣ�
        url="http://"+str(url)
        request = urllib2.Request(url, datagen, headers)
        # ʵ��ִ������ȡ�÷���
        return urllib2.urlopen(request).read()

    #�ж��Ƿ�ִ�б���
    def is_exec(self,table_in,nrow_in,label):
        exec_str1 = table_in.cell(nrow_in,self.is_exec_col).value
        exec_str2 = table_in.cell(nrow_in,self.is_exec_type_col).value
        #self.logstu.debug(u"testcase��Ĳ���������:"+label)
        #self.logstu.debug(u"appin��Ĳ���������:"+exec_str2)
        if exec_str1 == u'��' and exec_str2 == label:
            return 1
        else:
            return -1

    #�����һ�β��Խ��
    def clear_data(self,row_in):
        self.logstu.debug(u"��ʼ�����ϴ�ִ�н��������------------")
        path =self.path
        recv_body_col = self.recv_body_col
        result_col = self.result_col
        sheetname = self.sheetname
        table_in = xlrd.open_workbook(path)
        newdatas = copy(table_in)
        newtable = newdatas.get_sheet(self.sheetindex)
        #data_in = unicode(str_in,"gbk")
        for i in range(1,row_in):
            newtable.write(i,recv_body_col,"")
            newtable.write(i,result_col,"")
        newdatas.save(path)

    #���ݿ����
    def oracle_opt(self,connstr,sqlstr):
        conn = cx_Oracle.connect(connstr)
        sqlstr = sqlstr.replace('"',"'")
        cursor = conn.cursor()
        cursor.execute(sqlstr)
        conn_res_str = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return conn_res_str

    #������� �����µ��ĵ���
    def reslut_opt(self,table_in,recv_str,i):
        if recv_str <> -1:
            self.write_file(unicode(recv_str,"gbk"),i,self.recv_body_col)  #д�뷵�ر��ĵ�Ӧ�Եı���У�i,ncols)
            self.is_pass(table_in,recv_str,i)  #�����Խ����¼�������
        else:
            self.write_file(unicode("���׳�ʱ","gbk"),i,self.recv_body_col)  #д�볬ʱ��Ϣ��i,ncols)
            self.is_pass(table_in,"���׳�ʱ",i)  #�����Խ����¼�������
        time.sleep(1)

    #ʵʱ��ȡ�������ʵʱ����
    def get_cell_value(self,row_in,colname):
        table_in = self.load_files(self.sheetname)
        savecol = self.get_key_cell_col(table_in,colname)
        self.logstu.debug(u"ȡ�����ֶε���ֵ��:" + str(savecol))
        valuetstr = table_in.cell(row_in,savecol).value
        return valuetstr

    def relust_log_print(self):
        sheetname = self.sheetname
        sys_env_col = self.sys_env_col
        case_name_col = self.case_name_col
        result_col = self.result_col
        table = self.load_files(sheetname)
        nrows = table.nrows
        last_reslut = 0
        self.logstu.debug( u"ϵͳ���� :     �������� :     ִ�н�� :   ")
        for j in range(1,nrows):
            if self.is_exec(table,j,self.dict_data[u'��������'.encode('utf-8')]) == 1 :
                self.logstu.debug(table.cell(j,sys_env_col).value + "    " + table.cell(j,case_name_col).value + "    " + table.cell(j,result_col).value)
                if table.cell(j,result_col).value =="PASS":
                    last_reslut = last_reslut + 1
        '''
        if last_reslut == 10:
            self.logstu.debug("last_all_status= :returncode=0")
            return 0
        else:
            self.logstu.debug("last_all_status= :returncode=-1")
            return -1
        '''
    def test_AppIn(self):
        self.logstu.info(u"����������app��������,Ԥ����Ҫ 8 ����ʱ��")
        self.cur_file_dir()
        table = self.read_comm_param()  #��ȡ��������
        nrows = table.nrows
        #self.clear_data(nrows) #����ϴβ��Խ��
        #self.relust_log_print()
        lastpostrcv = ""
        time.sleep(1)
        for i in range(1,nrows): #i ��ʾ���ڴ��������
            self.logstu.debug(self.dict_data[u'��������'.encode('utf-8')])
            exec_row = self.is_exec(table,i,self.dict_data[u'��������'.encode('utf-8')])
            if exec_row == 1:
                self.logstu.debug( u"���׿�ʼ  ---  " + time.strftime('%Y-%m-%d %X',time.localtime()))
                reqstr,sendstr=self.read_request(table,i) #��ȡ�����ַ�ͱ����ڲ�
                self.write_file(sendstr,i,self.send_body_col) #�����ͱ��ı��浽�ļ���
                self.logstu.debug(u"���ͱ�����:")
                self.logstu.debug(sendstr.encode("utf-8"))
                sendstr = sendstr.encode("gbk")
                #sendstr = unicode(sendstr.encode("utf-8"),encoding="gbk",errors="strict")
                self.logstu.debug(u"���ձ�����:")
                type_str=table.cell(i,self.exec_type_col).value #�ж�������Э�鷽ʽ����
                if type_str == "httpPost":
                    rcvstr = self.http_post_send(reqstr,sendstr)
                    self.logstu.debug(unicode( rcvstr,encoding="gbk",errors='ignore').encode("utf-8"))
                    self.reslut_opt(table,rcvstr,i)
                    time.sleep(1)
                if type_str == "httpPostFile":
                    rcvstr = self.http_post_file_send(reqstr,sendstr)
                    self.logstu.debug(unicode( rcvstr,encoding="gbk",errors='ignore').encode("utf-8"))
                    self.reslut_opt(table,rcvstr,i)
                    time.sleep(1)
                if type_str == "sql":
                    rcvstr = self.oracle_opt(reqstr,sendstr)
                    rcvstr = str(rcvstr).decode('string_escape')
                    self.logstu.debug(unicode( rcvstr,encoding="gbk",errors='ignore').encode("utf-8"))
                    self.reslut_opt(table,rcvstr,i)
                #���з��ر���������к�ͬ���ֶεĴ�ӡ���� ����¼����־��
                savekeystr = self.get_cell_value(i,"�����ֶ�")
                self.logstu.info(u'��Ҫ������ֶ�����:' + savekeystr)
                if ( savekeystr in rcvstr) and savekeystr <> "" :
                    tpht = rcvstr.split(savekeystr+'":"')
                    tpht1 = tpht[1].split('","')
                    savevaluestr = tpht1[0]
                    self.logstu.info(u'��Ҫ������ֶ�����:' + savekeystr)
                    self.logstu.info(u'��Ҫ������ֶ�ֵ��:' + savevaluestr)
                    self.comm.write_file(savevaluestr,self.row,self.comm.get_key_cell_col(u"ִ�н��"))
                    self.logstu.info(u"app��������ɹ�,���������ĺ�ͬ��д��ִ�н����")
        #�����ս��д����־��
        restatus = self.relust_log_print()

