# -*- coding: utf-8 -*-
from urllib import urlencode
import httplib2, re, sys, os,ssl, urllib,urllib2, time,cookielib,httplib,json
import requests, logging
from logger import Logger
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
reload(sys)
sys.setdefaultencoding('utf-8')

class HttpAct(object):
    myhead = {u'User-Agent':u'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
              u'Content-Type': u'application/x-www-form-urlencoded',
              u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              u'Connection':u'keep-alive'}
    iCookie = ''    # 字符串格式， xxx=xxxxx; nnn=nnnnnnn
    i_aoID = ''     # 系统url后面的aoID
    isloaction = '' # 字符串格式， http://www.baidu.com
    h = ''          # 对象httplib2.Http()
    iCookie_jar = cookielib.CookieJar()
    request_session = None # requests.Session()
    url_host = ''
    url_params = ''

    # 单例模式创建driver
    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super(HttpAct, cls).__new__(cls)
            cls.logstu = Logger(sys.path[0] + '/logs/autotest.log', logging.DEBUG, logging.DEBUG)
            cls.h = httplib2.Http(timeout=120)  # '.cache'
            cls.h = httplib2.Http(disable_ssl_certificate_validation=True)
            cls.iCookie_jar = cookielib.CookieJar()
            cls.request_session = requests.Session()
        return cls.instance

    # 获取url中的host, 必须要有http:// 才能正常工作
    def get_hosturl(self, url):
        proto, rest = urllib.splittype(url)
        res, rest = urllib.splithost(rest)
        return res, rest
    # 手动添加 cookie
    def make_cookie(self,name, value, path = '/', hosturl = ''):
        return cookielib.Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=hosturl,
            domain_specified=True,
            domain_initial_dot=False,
            path=path,
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None
        )

    # 根据返回的头部信息的 set-cookie 更新cookie
    def i_set_cookie(self, resp):
        if 'set-cookie' in resp:
            for bigcookie in resp['set-cookie'].split(','):
                bigcookie = bigcookie.strip()
                cookie_key = u''
                cookie_value = u''
                cookie_path = u'/'
                for newcookie in bigcookie.split(';'):
                    if newcookie.split('=')[0].strip().upper() == 'path'.upper():
                        cookie_path = newcookie.split('=')[1].strip()
                        continue
                    if newcookie.split('=')[0].strip().upper() == 'expires'.upper() \
                            or newcookie.find('=') == -1:
                        continue
                    cookie_key = newcookie[:newcookie.find('=')]
                    cookie_value = newcookie[newcookie.find('=') + 1:]
                    if cookie_key != '':
                        self.iCookie_jar.set_cookie(self.make_cookie(cookie_key,cookie_value,cookie_path,self.url_host))
                    if self.iCookie == '':
                        self.iCookie = self.iCookie + newcookie
                    if self.iCookie.find(newcookie.split('=')[0]) == -1:
                        self.iCookie = self.iCookie + ';' + newcookie
                    else:
                        search_rul = re.search(newcookie.split('=')[0] + r'(.*?);', self.iCookie, re.M | re.I)
                        if search_rul == None:
                            search_rul = re.search(newcookie.split('=')[0] + r'(.*?)$', self.iCookie, re.M | re.I)
                            if search_rul == None:
                                continue
                            else:
                                self.iCookie = self.iCookie.replace(search_rul.group(), newcookie)
                        else:
                            self.iCookie = self.iCookie.replace(
                                re.search(newcookie.split('=')[0] + r'(.*?);', self.iCookie, re.M | re.I).group(),
                                newcookie + ';')
        self.myhead[u'Cookie'] = self.iCookie
        #self.logstu.debug(self.iCookie)
        return self.iCookie

    # 自动跳转，依据响应头部的Location字段，有个问题是跳转后还有这个字段，原因不明，所以增加判断只跳一次
    # iurl 源url地址，根据这个判断跳转是否还是同一个地址，相同则不再跳转，实际测试发现有些url get了但是又跳转一次导致失败
    def i_content_location(self, resp, iurl):
        if resp.has_key('content-location'):
           # if resp['content-location'].find('http://') == -1:

            if resp['content-location'] == self.isloaction:
                return (resp,'')
            if resp['content-location'] == iurl:
                return (resp, '')
            if resp['content-location'].find('aoID=') != -1:
                self.i_aoID = resp['content-location'].decode('gbk').split('aoID=')[1]
                self.logstu.debug(resp['content-location'])
            self.isloaction = resp['content-location']
            (resp, context) = self.get_http_request(self.isloaction)
            return (resp, context)
        if resp.has_key('location'):
            if resp['location'] == iurl:
                return (resp, '')
            if resp['location'].find('aoID=') != -1:
                self.i_aoID = resp['location'].decode('gbk').split('aoID=')[1]
                self.logstu.debug(resp['location'])
            self.isloaction = resp['location']
            (resp, context) = self.get_http_request(self.isloaction)
        return (resp,'')

    # 保存图片功能
    def save_file(self, file_name, data):
        if data == None:
            return
        if os.path.exists(file_name) == False:
            p, f = os.path.split(file_name);
            if os.path.exists(p) == False:
                os.makedirs(p)
        file = open(file_name, "wb")
        file.write(data)
        file.flush()
        file.close()
    # get 请求，有自动跳转功能，并调用自动更新cookie方法
    # ihead参数为 key=value形式，设置head
    def get_http_request(self, iurl, *ihead):
        gethead = self.myhead
        self.url_host, self.url_params = self.get_hosturl(iurl) # 解析中host和后面的接口参数部分
        if self.h == '':
            self.h = httplib2.Http()
        if len(ihead) > 0:
            for ih in ihead:
                gethead[ih.split('=')[0]] = ih.split('=')[1]
        resp, content = self.h.request(iurl,headers=gethead)

        is_api_change = 0
        if (int(resp['status']) >= 400 and int(resp['status']) < 500) or content.find('javax.servlet.ServletException') != -1:
            resp, content = self.get_http_requests(iurl, *ihead)
            is_api_change = 1
        if (int(resp['status']) >= 400 and int(resp['status']) < 500) or content.find('javax.servlet.ServletException') != -1:
            resp, content = self.get_http_urllib2(iurl, *ihead)
            is_api_change = 2
        if (int(resp['status']) >= 400 and int(resp['status']) < 500) or content.find('javax.servlet.ServletException') != -1:
            resp, content = self.get_http_httplib(iurl)
            is_api_change = 3

        if self.myhead.has_key('Referer'):
            del self.myhead['Referer']
        if is_api_change > 0:
            return resp, content

        self.i_set_cookie(resp)
        idecode = 'UTF-8'
        if resp.has_key('content-type'):
            if resp['content-type'].find('charset=') != -1:
                idecode = resp['content-type'][resp['content-type'].find('charset=') + 8:]
            self.logstu.debug('当前响应信息编码格式为：%s | 截取编码：%s' % (resp['content-type'], idecode))
        if resp.has_key('content-disposition'):
            if resp['content-disposition'].find('filename') != -1:
                filename = resp['content-disposition'][resp['content-disposition'].find('=') + 1:]
                self.save_file('output/'+ filename, content)
                return (resp, 'output/'+ filename)
        return (resp, content.decode(idecode, 'ignore').strip())

    def get_http_httplib(self, iurl):
        self.url_host, self.url_params = self.get_hosturl(iurl)  # 解析中host和后面的接口参数部分
        resp = {}
        content = ''
        httpClient = None
        try:
            host = self.url_host
            params = self.url_params
            port = 80
            if host.find(':') != -1:
                host = self.url_host[:self.url_host.find(':')]
                port = int(self.url_host[self.url_host.find(':')+1:])
            httpClient = httplib.HTTPConnection(host, port, timeout=120)
            httpClient.request('GET', params,headers=self.myhead)
            response = httpClient.getresponse() # response是HTTPResponse对象

            for (key, value) in  response.getheaders():
                resp[key] = value
            resp['status'] = response.status
            content = response.read()
            # 重定向
            if response.status == 302:
                Location = response.getheader('Location', '')
                if Location.find('http') == -1 and Location.find(host) == -1:
                    Location = 'http://'+ host + Location
                if Location.find('http') == -1 and Location.find(host) != -1:
                    Location = 'http://' + Location
                resp, content = self.get_http_httplib(Location)
        except Exception, e:
            content = str(e)
            self.logstu.debug(e)
        finally:
            if httpClient:
                httpClient.close()
            return resp,content

    # ihead参数为 key=value形式，设置head
    # post方法请求页面，自动更新cookie和跳转页面, 使用效率最高的 httplib2
    def post_http_request(self, iurl, idata, *ihead):
        self.url_host, self.url_params = self.get_hosturl(iurl)  # 解析中host和后面的接口参数部分
        posthead = self.myhead
        #posthead['Content-Type'] = 'application/x-www-form-urlencoded'
        if self.h == '':
            self.h = httplib2.Http(timeout=120)
        if self.iCookie != '':
            posthead['Cookie'] = self.iCookie
        if len(ihead) > 0:
            for ih in ihead:
                posthead[ih.split('=')[0]] = ih.split('=')[1]
        (resp, content) = self.h.request(iurl,'POST',urlencode(idata),headers=posthead)

        is_api_change = 0
        if (int(resp['status']) >= 400 and int(resp['status']) < 500) or content.find('javax.servlet.ServletException') != -1:
            resp, content = self.post_http_requests(iurl, idata, *ihead)
            is_api_change = 1
        if (int(resp['status']) >= 400 and int(resp['status']) < 500) or content.find('javax.servlet.ServletException') != -1:
            resp, content = self.post_http_urllib2(iurl, idata, *ihead)
            is_api_change = 2

        if self.myhead.has_key('Referer'):
            del self.myhead['Referer']
        if is_api_change > 0:
            return resp, content

        self.i_set_cookie(resp)

        idecode = 'UTF-8'
        if resp.has_key('content-type'):
            if resp['content-type'].find('charset=') != -1:
                idecode = resp['content-type'][resp['content-type'].find('charset=') + 8:]
            self.logstu.debug('当前响应信息编码格式为：%s | 截取编码：%s' % (resp['content-type'],idecode))
        return (resp, content.decode(idecode,'ignore').strip())

    # requests mode   post_http_request_requests
    def post_http_requests(self, iurl, idata, *ihead):
        posthead = self.myhead
        if len(ihead) > 0:
            for ih in ihead:
                posthead[ih.split('=')[0]] = ih.split('=')[1]
        if self.iCookie_jar == None or len(self.iCookie_jar) == 0:
            r = self.request_session.post(iurl,urlencode(idata),headers=posthead)
        else:
            r = self.request_session.post(iurl,urlencode(idata),headers=posthead,cookies = self.iCookie_jar)

        if 'Set-Cookie' in r.headers:
            self.i_set_cookie(r.headers)
            if len(r.cookies) > 0:
                for cookie_i in r.cookies:
                    self.iCookie_jar.set_cookie(cookie_i)
        resp = r.headers
        resp['status'] = r.status_code
        resp['cookies'] = r.cookies
        resp['apparent_encoding'] = r.apparent_encoding
        return (resp, r.text)

    # 使用urllib2模块完成post json请求
    def post_http_urllib2_json(self, iurl, idata, *ihead):
        posthead = {}#self.myhead
        '''
        if self.iCookie != '':
            posthead['Cookie'] = self.iCookie
        if len(ihead) > 0:
            for ih in ihead:
                posthead[ih.split('=')[0]] = ih.split('=')[1]
        '''
        posthead[u'Content-Type'] = u'application/json; charset=utf-8'
        idata = {
                "merchantCode":"R220232",
                "signId":"st6KNKquEVW2r+s1+lNRPFaKfJXLJofo5ttEkDbQ1vc/CwWC1OIBYkOOJ7f7Q8V9KgiZQolZXdsGqiheiJc7ILJ8zwtM/ivhuOE4lKquRjIaIOnlmdzHHZKcmGYwApzHyghyqhnUdz5nwCh9ZWd37KM/Lj0YEAbHBv7tYOJHxB4= ",
                "isSdk":"true"
                }
        jdata = urllib.urlencode(idata)
        #jdata = json.dumps(idata)  # 对数据进行JSON格式化编码
        req = urllib2.Request(iurl, jdata,headers=posthead)
        try:
            response = urllib2.urlopen(req, timeout=120)
        except urllib2.HTTPError as e:
            self.logstu.error(e)
            resp = {'status': 409}
            return resp, str(e)
        posthead[u'Content-Type'] = u'application/x-www-form-urlencoded'
        resp = response.headers
        resp['status'] = str(response.code)
        content = response.read()
        self.i_set_cookie(resp)
        if hasattr(req, 'redirect_dict'):
            for redirect in req.redirect_dict:
                resp['redirect_dict' + str(req.redirect_dict[redirect])] = redirect
        idecode = 'UTF-8'
        if resp.has_key('content-type'):
            idecode = resp['content-type'][resp['content-type'].find('charset=') + 8:]
            self.logstu.debug('当前响应信息编码格式为：%s | 截取编码：%s' % (resp['content-type'], idecode))
        return (resp, content.decode(idecode, 'ignore').strip())

    # 发送json数据
    def post_http_requests_json(self, iurl, idata, *ihead):
        posthead = {}  # self.myhead
        if len(ihead) > 0:
            for ih in ihead:
                posthead[ih.split('=')[0]] = ih.split('=')[1]
        posthead[u'Content-Type'] = u'application/json; charset=utf-8'
        jdata = self.logstu.all_type_to_encode(idata) # 将uncode字符串编码为utf8，否则有中文可能导致后台验证失败
        try:
            if self.iCookie_jar == None or len(self.iCookie_jar) == 0:
                r = requests.post(iurl, data=jdata, headers=posthead)
            else:
                r = requests.post(iurl, data=jdata, headers=posthead, cookies=self.iCookie_jar)
        except Exception as e:
            self.logstu.error(e)

        posthead[u'Content-Type'] = u'application/x-www-form-urlencoded'
        if 'Set-Cookie' in r.headers:
            self.i_set_cookie(r.headers)
            if len(r.cookies) > 0:
                for cookie_i in r.cookies:
                    self.iCookie_jar.set_cookie(cookie_i)
        resp = r.headers
        resp['status'] = r.status_code
        resp['cookies'] = r.cookies
        resp['apparent_encoding'] = r.apparent_encoding
        return (resp, r.text)

    # 使用urllib2模块完成post请求
    def post_http_urllib2(self, iurl, idata, *ihead):
        posthead = self.myhead
        if self.iCookie != '':
            posthead['Cookie'] = self.iCookie
        if len(ihead) > 0:
            for ih in ihead:
                posthead[ih.split('=')[0]] = ih.split('=')[1]
        req = urllib2.Request(iurl, urllib.urlencode(idata), headers=posthead)
        try:
            response = urllib2.urlopen(req,timeout=120)
        except urllib2.HTTPError as e:
            self.logstu.error(e)
            resp = {'status': 409}
            return resp, str(e)

        resp = response.headers
        resp['status'] = str(response.code)
        content = response.read()
        self.i_set_cookie(resp)
        if hasattr(req, 'redirect_dict'):
            for redirect in req.redirect_dict:
                resp['redirect_dict' + str(req.redirect_dict[redirect])] = redirect
        idecode = 'UTF-8'
        if resp.has_key('content-type'):
            idecode = resp['content-type'][resp['content-type'].find('charset=') + 8:]
            self.logstu.debug('当前响应信息编码格式为：%s | 截取编码：%s' % (resp['content-type'], idecode))
        return (resp, content.decode(idecode, 'ignore').strip())

    # 使用requests模块完成get请求, 注意：httplib2执行速度快但有的请求失败返回状态400， urllib2倒是成功了但速度很慢有些需要9s才响应
    def get_http_requests(self, iurl, *ihead):
        posthead = self.myhead
        if self.iCookie != '':
            posthead['Cookie'] = self.iCookie
        if len(ihead) > 0:
            for ih in ihead:
                posthead[ih.split('=')[0]] = ih.split('=')[1]
        if self.iCookie_jar == None or len(self.iCookie_jar) == 0:
            #r = requests.get(iurl, headers=posthead, timeout = 120)
            r = self.request_session.get(iurl, headers=posthead, timeout = 120)
        else:
            #r = requests.get(iurl, cookies= self.iCookie_jar,timeout=120)
            r = self.request_session.get(iurl,headers=posthead, cookies= self.iCookie_jar,timeout=120)
        if 'Set-Cookie' in r.headers:
            self.i_set_cookie(r.headers)
            if len(r.cookies) > 0:
                for cookie_i in r.cookies:
                    self.iCookie_jar.set_cookie(cookie_i)
        #self.logstu.debug(r.text)
        resp = r.headers
        resp['status'] = r.status_code
        resp['cookies'] = r.cookies
        resp['apparent_encoding'] = r.apparent_encoding

        if hasattr(resp, 'redirect_dict'):
            for redirect in resp.redirect_dict:
                resp['redirect_dict' + str(resp.redirect_dict[redirect])] = redirect

        self.i_set_cookie(resp)
        idecode = 'UTF-8'
        if 'content-type' in resp:
            if resp['content-type'].find('charset=') != -1:
                idecode = resp['content-type'][resp['content-type'].find('charset=') + 8:]
            self.logstu.debug('当前响应信息编码格式为：%s | 截取编码：%s' % (resp['content-type'], idecode))
        if 'Content-Disposition' in resp:
            if resp['content-disposition'].find('filename') != -1:
                filename = resp['content-disposition'][resp['content-disposition'].find('=') + 1:]
                self.save_file('output/' + filename, r.content)
                return (resp, 'output/' + filename)
        return (resp, r.text)

    # 使用urllib2模块完成get请求
    def get_http_urllib2(self, iurl, *ihead):
        posthead = self.myhead
        if self.iCookie != '':
            posthead['Cookie'] = self.iCookie
        if len(ihead) > 0:
            for ih in ihead:
                posthead[ih.split('=')[0]] = ih.split('=')[1]
        req = urllib2.Request(iurl, headers=posthead)
        response = urllib2.urlopen(req)
        resp = response.headers
        resp['status'] = str(response.code)
        if hasattr(req, 'redirect_dict'):
            for redirect in req.redirect_dict:
                resp['redirect_dict'+ str(req.redirect_dict[redirect])] = redirect
        content = response.read()  # resp
        self.i_set_cookie(resp)
        idecode = 'UTF-8'
        if resp.has_key('content-type'):
            idecode = resp['content-type'][resp['content-type'].find('charset=') + 8:]
            self.logstu.debug('当前响应信息编码格式为：%s | 截取编码：%s' % (resp['content-type'], idecode))
        return (resp, content.decode(idecode, 'ignore').strip())

    # 上传附件和post数据
    def upfile_requests(self, url, data, upfilepath):
        p, f = os.path.split(upfilepath);
        if upfilepath.find('=') != -1:
            files = {upfilepath[:upfilepath.find('=')]: open(upfilepath[upfilepath.find('=') + 1:], 'rb')}
        else:
            #files = {'file': (f, open(upfilepath, 'rb'))}
            files = {'file': open(upfilepath, 'rb')}#files = {f: (f, open(upfilepath, 'rb'))}  # 显式的设置文件名

        #self.myhead['Content-Type'] = 'multipart/form-data'
        if self.iCookie_jar == None or len(self.iCookie_jar) == 0:
            r = self.request_session.post(url, files=files, data=data, timeout=30) # self.request_session
        else:
            r = self.request_session.post(url,files=files, data=data, headers={'Cookie':self.myhead['Cookie']}, timeout=30) #, cookies=self.iCookie_jar
        self.logstu.debug(r.text)
        self.myhead['Content-Type'] = 'application/x-www-form-urlencoded'
        upfilehead = {}
        upfilehead['status'] = r.status_code
        upfilehead['cookies'] = r.cookies
        upfilehead['apparent_encoding'] = r.apparent_encoding
        return (upfilehead, r.text)

    # 上传附件和post数据
    def upfile_urllib2(self, url, data, upfilepath):
        #encode_json = json.dumps(data)
        #encode_json = self.logstu.all_type_to_encode_gbk(encode_json)
        #data = json.loads(encode_json)
        # 在 urllib2 上注册 http 流处理句柄
        register_openers()
        if upfilepath.find('=') != -1:
            data[upfilepath[:upfilepath.find('=')]] = open(upfilepath[upfilepath.find('=')+1:], "rb")
        else:
            data['file'] = open(upfilepath, "rb") #file

        # 开始对文件 "DSC0001.jpg" 的 multiart/form-data 编码
        # "image1" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置
        # headers 包含必须的 Content-Type 和 Content-Length
        # datagen 是一个生成器对象，返回编码过后的参数
        datagen, headers = multipart_encode(data)
        if self.myhead.has_key('Cookie'):
            if self.myhead['Cookie'] != '':
                headers['Cookie'] = self.myhead['Cookie']
        self.myhead['Content-Type'] = 'multipart/form-data'
        ssl._create_default_https_context = ssl._create_unverified_context # 关闭ssl验证
        request = urllib2.Request(url, datagen, headers)
        response_data = urllib2.urlopen(request, timeout = 120)
        result = response_data.read()
        response_data.headers.dict['status'] = str(response_data.code)

        self.myhead['Content-Type'] = 'application/x-www-form-urlencoded'
        if self.myhead.has_key('Referer'):
            del self.myhead['Referer']

        idecode = 'UTF-8'
        if response_data.headers.dict.has_key('content-type'):
            idecode = response_data.headers.dict['content-type'][response_data.headers.dict['content-type'].find('charset=') + 8:]
            self.logstu.debug('当前响应信息编码格式为：%s | 截取编码：%s' % (response_data.headers.dict['content-type'], idecode))
        return (response_data.headers.dict, result.decode(idecode, 'ignore').strip())
        #return (response_data.headers.dict, result)


if __name__ == '__main__':
    myhttp = HttpAct()
    print myhttp.iCookie_jar
    myhttp.iCookie_jar.set_cookie(myhttp.make_cookie('JSESSIONID','3EE26A5B1E291DBC4E5F1C4CDA55A09A',u'/','127.0.0.1'))
    print myhttp.iCookie_jar
    '''
    data = {'Password': 'xiaoniu@2016',
            'ScreenWidth': '1366',
            'UserID': 'SN00107',
            'iscity': 'ISCITY'}
    isMain = myhttp.post_http_request('http://10.20.2.12:7001/XiaoNiu/Logon.jsp', data)
    if isMain.find('window.open("/XiaoNiu/Redirector?ComponentURL=/Main.jsp"') != -1:
        myhttp.get_http_request('http://10.20.2.12:7001/XiaoNiu/Redirector?ComponentURL=/Main.jsp')
    myhttp.get_http_request('http://10.20.2.12:7001/XiaoNiu/Redirector?OpenerClientID=' +
                            myhttp.i_aoID + '&ComponentURL=/DeskTop/WorkTips.jsp&_SYSTEM_MENU_FALG=0')
    myhttp.get_http_request('http://10.20.2.12:7001/XiaoNiu/Redirector?OpenerClientID='
                            + myhttp.i_aoID + '&ComponentURL=/DeskTop/MyCalendar.jsp')

    print myhttp.get_http_request('http://10.20.2.12:7001/XiaoNiu/Redirector?OpenerClientID='
                            + myhttp.i_aoID + '&ComponentURL=/BusinessManage/RetailManage/StoreAttachmentChooseDialog.jsp'
                            + '&Type=6001&ObjectNo=2016062400000006')

    print ('------------upload File Start------------')
    #boundary = '----------%s' % hex(int(time.time() * 1000))
    #myhttp.myhead['Content-Type'] = 'multipart/form-data; boundary=%s' % boundary
    myhttp.myhead['Content-Type']='multipart/form-data;' # 上传文件的Content-Type
    print myhttp.myhead['Content-Type']
    #myhttp.myhead['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    # post携带的数据
    data = {}
    data['CompClientID'] = myhttp.i_aoID
    data['Type'] = '6001'
    data['ObjectNo'] = '2016062400000006'
    data['FileName'] = '1.jpg'
    upurl = 'http://10.20.2.12:7001/XiaoNiu/BusinessManage/StoreManage/StoreAttachmentUpload.jsp?CompClientID=' + myhttp.i_aoID
    upfilerul = myhttp.upfile_requests(upurl, data, '../../../images/1.jpg')
    print upfilerul
'''




