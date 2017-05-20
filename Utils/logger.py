#coding=utf8
import logging,os, sys, types, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Logger(object):
    # 单例模式创建driver
    def __new__(cls, logpath='', clevel=logging.DEBUG, Flevel=logging.DEBUG):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            if logpath == '':
                logpath = os.getcwd() + '/logs/autotest.log';
            if os.path.exists(logpath) == False:
                p, f = os.path.split(logpath);
                if os.path.exists(p) == False:
                    os.makedirs(p)
            cls.instance = super(Logger, cls).__new__(cls)
            cls.logger = logging.getLogger(logpath)  # path
            cls.logger.setLevel(logging.DEBUG)
            fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
            # 设置CMD日志
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)
            sh.setLevel(clevel)
            # 设置文件日志
            fh = logging.FileHandler(logpath)
            fh.setFormatter(fmt)
            fh.setLevel(Flevel)
            cls.logger.addHandler(sh)
            cls.logger.addHandler(fh)
        return cls.instance

    # 判断字符串是否有unicode，如果有解码为utf8格式(解决jenkins中文乱码问题)
    def all_type_to_encode(self, value):
        if isinstance(value, unicode):
            return value.encode('UTF-8')
        if type(value) == types.ListType or type(value) == types.TupleType or type(value) == types.DictType:
            return json.dumps(value, encoding='UTF-8', ensure_ascii=False)
        return value

    # send_keys发送汉字要 unicode格式，这里统一修改
    def all_type_to_unicode(self, str_in):
        # 处理字符编码问题
        if isinstance(str_in, float):
            pass
        elif isinstance(str_in, unicode):
            pass
        else:
            str_in = unicode(str_in, "UTF-8")
        return str_in

    def debug(self,message):
        self.logger.debug(self.all_type_to_encode(message))

    def info(self,message):
        self.logger.info(self.all_type_to_encode(message))

    def war(self,message):
        self.logger.warn(self.all_type_to_encode(message))

    def error(self,message):
        self.logger.error(self.all_type_to_encode(message))

    def cri(self,message):
        self.logger.critical(self.all_type_to_encode(message))

    def debug_gkb(self, message):
        self.logger.debug(self.all_type_to_encode_gbk(message))

if __name__ =='__main__':
    logyyx = Logger('autotest.log',logging.DEBUG,logging.DEBUG)
    logyyx2 = Logger('autotest.log', logging.DEBUG, logging.DEBUG)
    logyyx.debug('一个debug信息')
    logyyx.debug({'哈哈哈来了':'和和abc', '2':u'我们', u'我':'12'})
    print id(logyyx)  # 29097904
    print id(logyyx2)  # 29097904
