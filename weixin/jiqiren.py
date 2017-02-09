#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
import random
from urllib import urlencode
 
#----------------------------------
# 图灵机器人调用示例代码
# 在线接口文档：http://www.juhe.cn/docs/112
#----------------------------------

#配置您申请的APPKey
appkey = "4db23df6938f42b59aeae27226cff3af"
apiurl = "http://www.tuling123.com/openapi/api"

def main(question,userid):
    #1.问答
    getAnswerByAI(question,userid,"GET")
 
 
#问答
def getAnswerByAI(query,userid, m="GET"):
    params = {
        "key" : appkey, #您申请到的本接口专用的APPKEY
        "info" : query, #要发送给机器人的内容，不要超过30个字符
        "dtype" : "json", #返回的数据的格式，json或xml，默认为json
        "loc" : "", #地点，如北京中关村
        "lon" : "", #经度，东经116.234632（小数点后保留6位），需要写为116234632
        "lat" : "", #纬度，北纬40.234632（小数点后保留6位），需要写为40234632
        "userid" : userid, #1~32位，此userid针对您自己的每一个用户，用于上下文的关联 
    }
    print 'getAnswerByAI ===== userid : ', userid
    print params
    params = urlencode(params)
    if m =="GET":
        f = urllib.urlopen("%s?%s" % (apiurl, params))
    else:
        f = urllib.urlopen(apiurl, params)
 
    content = f.read()
    print 'content : ', content
    res = json.loads(content)
    print res
    result = {}
    if res:
        result_code = res["code"]
        #print "%s:%s" % (res["code"],res["text"])
        if result_code == 100000 :
            #成功请求
            result['responseType'] = 'text'
            result['content'] = res["text"]
            result['result_code'] = result_code
        elif result_code == 200000 :
            result['responseType'] = 'url'
            result['content'] = res["text"]
            result['url'] = res["url"]
            result['result_code'] = result_code
        elif result_code == 302000 :
            result['responseType'] = 'article'
            result['result_code'] = result_code
            articlejson = res["list"]
            articleselected = None
            if len(articlejson) > 5 :
                articleselected = random.sample(articlejson, 5)
            else :
                articleselected = articlejson
            articles = []
            if articleselected is not None :
                for news in articleselected:
                    article = {}
                    article['title'] = news['article']
                    article['description'] = news['article']
                    article['picurl'] = news['icon']
                    article['url'] = news['detailurl']
                    articles.append(article)
            print articles
            result['content'] = articles
        elif result_code == 308000 :
            result['responseType'] = 'article'
            result['result_code'] = result_code
            articlejson = res["list"]
            articleselected = None
            if len(articlejson) > 5:
                articleselected = random.sample(articlejson, 5)
            else:
                articleselected = articlejson
            articles = []
            if articleselected is not None:
                for news in articleselected:
                    article = {}
                    article['title'] = news['name']
                    article['description'] = news['info']
                    article['picurl'] = news['icon']
                    article['url'] = news['detailurl']
                    articles.append(article)
            print articles
            result['content'] = articles
        else:
            result['responseType'] = 'text'
            result['content'] = res["text"]
            result['result_code'] = result_code

    else:
        print "request api error"
        reply_text = "request api error"
        result['responseType'] = 'text'
        result['content'] = 'request api error'
        result['result_code'] = 'error'

    print result
    return result
 
# if __name__ == '__main__':
#     query = raw_input("请输入你的问题: ")
#     main(query,'userid')
