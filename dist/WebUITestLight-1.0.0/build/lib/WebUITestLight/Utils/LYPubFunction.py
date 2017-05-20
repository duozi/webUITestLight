# -*- coding: UTF-8 -*-
import random, types, json

# 独立的公共方法集合
class LYPubFunction(object):
    # 判断字符串是否有unicode，如果有解码为utf8格式
    def all_type_to_encode(self, value):
        if isinstance(value, unicode):
            return value.encode('utf8')
        else:
            return value

    # send_keys发送汉字要 unicode格式，这里统一修改
    def all_type_to_unicode(self, str_in):
        # 处理字符编码问题
        if isinstance(str_in, float):
            pass
        elif isinstance(str_in, unicode):
            pass
        else:
            str_in = unicode(str_in, "utf-8")
        return str_in

    # 判断字符串是否有unicode，如果有解码为utf8格式(解决jenkins中文乱码问题)
    def all_type_to_encode(self, value):
        if isinstance(value, unicode):
            return value.encode('UTF-8')
        if type(value) == types.ListType or type(value) == types.TupleType or type(value) == types.DictType:
            return json.dumps(value, encoding='UTF-8', ensure_ascii=False)
        return value

    # 用于产生随机汉字
    def GB2312(self):
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0, 0xF)
        val = (head << 8) | (body << 4) | tail
        str = "%x" % val
        return str.decode('hex').decode('gbk')

    # 字典key替换，用dict2的value替换dict1的key，
    # 如果dict2中有dict1没有则输出Not Found key[%s:%s]，
    # dict2没有的不会输出，丢掉了
    def dict_key_update(self, dict1, dict2):
        dict3 = {}
        for i in dict2:
            if dict2[i] in dict1.keys():
                dict3[i] = dict1[dict2[i]]
            else:
                dict3[i] = 'Not Found key[%s:%s]' % (i, dict2[i])
        return dict3
    # 为兼容以前的excel版本，将db查询结果none修改为 '' 空字符串类型
    def dict_None_to_Str(self, listdict):
        for dict in range(0, len(listdict)):
            for i in listdict[dict]:
                if type(listdict[dict][i]) == types.NoneType:
                    listdict[dict][i] = ''
        return listdict


if __name__ =='__main__':

    pubf = LYPubFunction()
    dict1 = [{
        'test_id':'test_id',
        'b':'2b2b',
        'c':None
    },{
        'a':'1a1a',
        'b':'2b2b',
        'c2':None
    }]

    print dict1
    c = pubf.dict_None_to_Str(dict1)
    print dict1[0]['test_id']