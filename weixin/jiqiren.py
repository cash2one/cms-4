#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
from urllib import urlencode
 
#----------------------------------
# 图灵机器人调用示例代码
# 在线接口文档：http://www.juhe.cn/docs/112
#----------------------------------
 
def main(question):
 
    #配置您申请的APPKey
    appkey = "4db23df6938f42b59aeae27226cff3af"
    apiurl = "http://www.tuling123.com/openapi/api"
 
    #1.问答
    request1(appkey,question,"GET") 
 
 
#问答
def request1(appkey,query, m="GET"):    
    params = {
        "key" : appkey, #您申请到的本接口专用的APPKEY
        "info" : query, #要发送给机器人的内容，不要超过30个字符
        "dtype" : "json", #返回的数据的格式，json或xml，默认为json
        "loc" : "", #地点，如北京中关村
        "lon" : "", #经度，东经116.234632（小数点后保留6位），需要写为116234632
        "lat" : "", #纬度，北纬40.234632（小数点后保留6位），需要写为40234632
        "userid" : "", #1~32位，此userid针对您自己的每一个用户，用于上下文的关联
 
    }
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (apiurl, params))
    else:
        f = urllib.urlopen(apiurl, params)
 
    content = f.read()
    print 'content : ', content
    res = json.loads(content)
    print 'res : ', res
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            print res["result"]
        else:
            print "%s:%s" % (res["error_code"],res["reason"])
    else:
        print "request api error"
 
 
if __name__ == '__main__':
    query = raw_input("raw_input: ")
    main(query)
