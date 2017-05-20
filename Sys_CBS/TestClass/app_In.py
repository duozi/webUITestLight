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
    sheetname = 'appin' #设置读取的sheet序号
    file_name = 'data/testcase.xls'
    sheetindex= 2
    dict_data = ''  # 接收main脚本传过来的参数
    mainWebDr = ""  # 接收main脚本付过来的
    comm = ""  # 接收main脚本传送的公共类实例对象
    row = ""  # 接收main脚本传送的当前处理的行数
    logstu = ""  # 接收main脚本传递来的写log的对象


    #获取当前路径
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

    # 读取文件数据   传sheet名字
    def load_files(self,sheetname):           # 读取文件数据
        #self.logstu.debug(self.path)
        #self.logstu.debug(sheetname)
        data = xlrd.open_workbook(self.path)
        table=data.sheet_by_name(sheetname)
        return table


    #读取列名对应的第几列  传表数据，列名
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
            self.logstu.debug(("没有取到： "+keyname_in+" ：对应的列数"))

    # 读取结构类型对应的列数，并返回整个sheet数据
    def read_comm_param(self):
        table = self.load_files(self.sheetname)
        self.recv_body_col = self.get_key_cell_col(table,'返回报文')
        self.send_body_col = self.get_key_cell_col(table,"发送报文")
        self.expect_result_col = self.get_key_cell_col(table,"预期结果")
        self.req_add_col = self.get_key_cell_col(table,"请求地址")
        self.result_col = self.get_key_cell_col(table,"验证结果")
        self.is_exec_col = self.get_key_cell_col(table,"是否执行")
        self.exec_type_col = self.get_key_cell_col(table,"执行方式")
        self.req_body_col = self.get_key_cell_col(table,"请求报文")
        self.case_name_col = self.get_key_cell_col(table,"案例名称")
        self.sys_env_col = self.get_key_cell_col(table,"系统环境")
        self.is_exec_type_col = self.get_key_cell_col(table,"操作类型")
        return table

    #读取前面存储的数据
    def get_above_str(self,table,need_read_str_in,row_in):
        recv_body_col = self.recv_body_col
        send_body_col = self.send_body_col
        sheetname = self.sheetname
        table_in = self.load_files(sheetname)
        find_col = 0
        need_read_str = str(need_read_str_in).decode('string_escape')
        tp_str1=need_read_str.split(')')
        up_now=int(tp_str1[0][5:])   #向上取的数据在第几行
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
        return keystr,valuestr.encode("GBK")   #返回查找的关键字+对应的值

    #读取请求报文,返回讲求地址+发送报文
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
        #读取请求地址
        urlstr=table_in.cell(row_in,req_add_col).value
        body_str=body_str.replace("$curedate",self.curedate)
        return urlstr,body_str

     #用于产生随机汉字
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

    # 写数据到对应的表格中
    def write_file(self,str_in,row_in,col_in):   #写入的数据“str_in” 一定要是，unicode类型
        path = self.path
        datas = xlrd.open_workbook(path)
        newdatas = copy(datas)
        newtable = newdatas.get_sheet(self.sheetindex)
        #data_in = unicode(str_in,"gbk")
        newtable.write(row_in,col_in,str_in)
        newdatas.save(path)
        self.logstu.debug(u'成功保存数据:  ' + str_in)

    #取预期的关键字
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
            self.logstu.debug(u"预期结果是="+str(yqstr))
        return yqstr

    #判断预期关键字，是否存在返回的结果中，如果在则PASS   如果不在则FAIL
    def is_pass(self,table_in,rcvstr_in,nrows_in):
        label = 0
        yq_str = self.get_yuqi_key(table_in,nrows_in)   #取得预期的关键字
        rcvstr_in = rcvstr_in.replace("'",'"')
        for i in range(len(yq_str)):
            if yq_str[i] in (unicode(rcvstr_in,"gbk")): #将测试结果记录到表格中
                label = label + 1
        if label == len(yq_str):
            self.logstu.debug("pass-------------")
            self.write_file('PASS',nrows_in,self.result_col)
        else :
            self.write_file('FAIL',nrows_in,self.result_col)
            self.logstu.debug("faile================")

    #发送httpPost报文
    def http_post_send(self,url,data_in):
        tp1 = url.split(',')
        ip = tp1[0]   #取目标地址
        serverstr = tp1[1]  #取服务名
        data_in = data_in.replace('"',"'")
        tms1 = eval("("+data_in+")") # 转换发送报文数据类型为dict
        params = urllib.urlencode(tms1)
        params = params.replace("5Cx","")  #处理中文字符的问题
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



    #发送httpPost_file报文
    def http_post_file_send(self,url,data_in):
        # 在 urllib2 上注册 http 流处理句柄
        register_openers()
        # 开始对文件 "DSC0001.jpg" 的 multiart/form-data 编码
        # "image1" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置
        # headers 包含必须的 Content-Type 和 Content-Length
        # datagen 是一个生成器对象，返回编码过后的参数
        datagen, headers = multipart_encode({"file": open(data_in, "rb")})
        add_headers = {"Authorization" : "Basic eGlhb25pdTpzdXBlcnNvbmlj","EncType":"multipart/form-data"}
        headers.update(add_headers)
        # 创建请求对象（localhost服务器IP地址，5000服务器端口）
        url="http://"+str(url)
        request = urllib2.Request(url, datagen, headers)
        # 实际执行请求并取得返回
        return urllib2.urlopen(request).read()

    #判断是否执行本行
    def is_exec(self,table_in,nrow_in,label):
        exec_str1 = table_in.cell(nrow_in,self.is_exec_col).value
        exec_str2 = table_in.cell(nrow_in,self.is_exec_type_col).value
        #self.logstu.debug(u"testcase里的操作类型是:"+label)
        #self.logstu.debug(u"appin里的操作类型是:"+exec_str2)
        if exec_str1 == u'是' and exec_str2 == label:
            return 1
        else:
            return -1

    #清除上一次测试结果
    def clear_data(self,row_in):
        self.logstu.debug(u"开始清理上次执行结果的数据------------")
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

    #数据库操作
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

    #结果处理 并更新到文档中
    def reslut_opt(self,table_in,recv_str,i):
        if recv_str <> -1:
            self.write_file(unicode(recv_str,"gbk"),i,self.recv_body_col)  #写入返回报文到应对的表格中（i,ncols)
            self.is_pass(table_in,recv_str,i)  #将测试结果记录到表格中
        else:
            self.write_file(unicode("交易超时","gbk"),i,self.recv_body_col)  #写入超时信息（i,ncols)
            self.is_pass(table_in,"交易超时",i)  #将测试结果记录到表格中
        time.sleep(1)

    #实时读取案例里的实时数据
    def get_cell_value(self,row_in,colname):
        table_in = self.load_files(self.sheetname)
        savecol = self.get_key_cell_col(table_in,colname)
        self.logstu.debug(u"取保存字段的例值是:" + str(savecol))
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
        self.logstu.debug( u"系统环境 :     案例名称 :     执行结果 :   ")
        for j in range(1,nrows):
            if self.is_exec(table,j,self.dict_data[u'操作类型'.encode('utf-8')]) == 1 :
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
        self.logstu.info(u"接下来进行app进件申请,预期需要 8 秒钟时间")
        self.cur_file_dir()
        table = self.read_comm_param()  #读取公共参数
        nrows = table.nrows
        #self.clear_data(nrows) #清楚上次测试结果
        #self.relust_log_print()
        lastpostrcv = ""
        time.sleep(1)
        for i in range(1,nrows): #i 表示正在处理的行数
            self.logstu.debug(self.dict_data[u'操作类型'.encode('utf-8')])
            exec_row = self.is_exec(table,i,self.dict_data[u'操作类型'.encode('utf-8')])
            if exec_row == 1:
                self.logstu.debug( u"交易开始  ---  " + time.strftime('%Y-%m-%d %X',time.localtime()))
                reqstr,sendstr=self.read_request(table,i) #读取请求地址和报文内部
                self.write_file(sendstr,i,self.send_body_col) #将发送报文保存到文件中
                self.logstu.debug(u"发送报文是:")
                self.logstu.debug(sendstr.encode("utf-8"))
                sendstr = sendstr.encode("gbk")
                #sendstr = unicode(sendstr.encode("utf-8"),encoding="gbk",errors="strict")
                self.logstu.debug(u"接收报文是:")
                type_str=table.cell(i,self.exec_type_col).value #判断用哪种协议方式运行
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
                #将有返回报文里存在有合同号字段的打印出来 并记录到日志中
                savekeystr = self.get_cell_value(i,"保存字段")
                self.logstu.info(u'需要保存的字段名是:' + savekeystr)
                if ( savekeystr in rcvstr) and savekeystr <> "" :
                    tpht = rcvstr.split(savekeystr+'":"')
                    tpht1 = tpht[1].split('","')
                    savevaluestr = tpht1[0]
                    self.logstu.info(u'需要保存的字段名是:' + savekeystr)
                    self.logstu.info(u'需要保存的字段值是:' + savevaluestr)
                    self.comm.write_file(savevaluestr,self.row,self.comm.get_key_cell_col(u"执行结果"))
                    self.logstu.info(u"app进件申请成功,并将产生的合同号写入执行结果中")
        #把最终结果写到日志上
        restatus = self.relust_log_print()

