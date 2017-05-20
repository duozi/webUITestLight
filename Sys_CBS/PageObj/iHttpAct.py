# -*- coding: utf-8 -*-
from urllib import urlencode
import httplib2, re, time, sys, os,urllib2,requests, logging
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from Utils.logger import Logger
reload(sys)
sys.setdefaultencoding('utf-8')

class IHttpAct(object):
    myhead = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
                   'Content-Type': 'application/x-www-form-urlencoded'}
    iCookie = ''    # 字符串格式， xxx=xxxxx; nnn=nnnnnnn
    i_aoID = ''     # 系统url后面的aoID
    isloaction = '' # 字符串格式， http://www.baidu.com
    h = ''          # 对象httplib2.Http()
    def __init__(self):
        # sys.path[0] + '/logs/autotest.log'
        self.logstu = Logger(sys.path[0] + '/logs/autotest.log', logging.DEBUG, logging.DEBUG)
        self.h = httplib2.Http() #'.cache'

    # 根据返回的头部信息的 set-cookie 更新cookie
    def i_set_cookie(self, resp):
        if resp.has_key('set-cookie'):
            for bigcookie in resp['set-cookie'].split(';'):
                bigcookie = bigcookie.strip()
                for newcookie in bigcookie.split(','):
                    #print 'old cookie:', self.iCookie
                    #print 'i_set_cookie for setcookie:\n\t',newcookie
                    if newcookie.split('=')[0] == 'expires' \
                            or newcookie.split('=')[0] == 'path'\
                            or newcookie.find('=') == -1:
                        continue
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
        self.myhead['Cookie'] = self.iCookie
        self.logstu.debug(self.iCookie)
        return self.iCookie

    # 自动跳转，依据响应头部的Location字段，有个问题是跳转后还有这个字段，原因不明，所以增加判断只跳一次
    def i_content_location(self, resp):
        if resp.has_key('content-location'):
            if resp['content-location'] == self.isloaction:
                return ''
            if resp['content-location'].find('aoID=') != -1:
                self.i_aoID = resp['content-location'].decode('gbk').split('aoID=')[1]
                self.logstu.debug(resp['content-location'])
            self.isloaction = resp['content-location']
            return self.get_http_request(self.isloaction)
        return ''

    # get 请求，有自动跳转功能，并调用自动更新cookie方法
    # ihead参数为 key=value形式，设置head
    def get_http_request(self, iurl, *ihead):
        gethead = self.myhead
        if self.h == '':
            self.h = httplib2.Http()
        if self.iCookie != '':
            gethead['Cookie'] = self.iCookie
        if len(ihead) > 0:
            for ih in ihead:
                gethead[ih.split('=')[0]] = ih.split('=')[1]
        resp, content = self.h.request(iurl,headers=gethead)
        self.logstu.debug('get响应的头部：\n%s' % (resp))
        #print 'get响应体内容：\n', content.decode('gbk'), '\n===================================='
        self.i_set_cookie(resp)
        is_location = self.i_content_location(resp)
        if is_location != '':
            return is_location
        return content #content.decode('gbk')

    # ihead参数为 key=value形式，设置head
    # post方法请求页面，自动更新cookie和跳转页面
    def post_http_request(self, iurl, idata, *ihead):
        posthead = self.myhead
        if self.h == '':
            self.h = httplib2.Http()
        if self.iCookie != '':
            posthead['Cookie'] = self.iCookie
        if len(ihead) > 0:
            for ih in ihead:
                posthead[ih.split('=')[0]] = ih.split('=')[1]
        resp, content = self.h.request(iurl,
                                  'POST',
                                  urlencode(idata),
                                  headers=posthead)
        self.logstu.debug('post响应的头部：\n%s'% resp)
        #print 'post响应体内容：\n', content.decode('gbk'), '\n===================================='
        self.i_set_cookie(resp)
        is_location = self.i_content_location(resp)
        if is_location != '':
            return is_location
        return content.decode('gbk')


    # 上传附件和post数据
    def upfile_requests(self, url, data, upfilepath):
        # 要上传的文件
        #files = {'1.jpg': ('1.jpg', open('output/1.jpg', 'rb'))}  # 显式的设置文件名
        p, f = os.path.split(upfilepath);
        if os.path.exists(upfilepath) == False:
            raise Exception(upfilepath + " Not Found." )
        files = {f: (f, open(upfilepath, 'rb'))}  # 显式的设置文件名
        self.myhead['Content-Type'] = 'multipart/form-data;'  # 上传文件的Content-Type
        r = requests.post(url, files=files, data=data, headers=self.myhead)
        self.myhead['Content-Type'] = 'application/x-www-form-urlencoded'
        return r.text


if __name__ == '__main__':
    myhttp = IHttpAct()
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





