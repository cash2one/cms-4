#/usr/bin/env python
#coding=utf8
import httplib
import urllib
import urllib2
import json

news_types = {
u"推荐新闻":"/touch/article/list/BA8J7DG9wangning/0-10.html",
u"头条新闻":"/touch/article/list/BBM54PGAwangning/0-2.html",
u"娱乐新闻":"/touch/article/list/BA10TA81wangning/0-10.html",
u"体育新闻":"/touch/article/list/BA8E6OEOwangning/0-10.html",
u"财经新闻":"/touch/article/list/BA8EE5GMwangning/0-10.html",
u"时尚新闻":"/touch/article/list/BA8F6ICNwangning/0-10.html",
u"军事新闻":"/touch/article/list/BAI67OGGwangning/0-10.html",
u"手机新闻":"/touch/article/list/BAI6I0O5wangning/0-10.html",
u"科技新闻":"/touch/article/list/BA8D4A3Rwangning/0-10.html",
u"游戏新闻":"/touch/article/list/BAI6RHDKwangning/0-10.html",
u"数码新闻":"/touch/article/list/BAI6JOD9wangning/0-10.html",
u"教育新闻":"/touch/article/list/BA8FF5PRwangning/0-10.html",
u"健康新闻":"/touch/article/list/BDC4QSV3wangning/0-10.html",
u"汽车新闻":"/touch/article/list/BA8DOPCSwangning/0-10.html",
u"家居新闻":"/touch/article/list/BAI6P3NDwangning/0-10.html",
u"房产新闻":"/touch/article/list/BAI6MTODwangning/0-10.html",
u"旅游新闻":"/touch/article/list/BEO4GINLwangning/0-10.html",
u"亲子新闻":"/touch/article/list/BEO4PONRwangning/0-10.html"
}

def getNews(news_type) :
    print 'news_type :', news_type
    httpClient = httplib.HTTPConnection('3g.163.com')
    news_url = news_types[news_type]
    httpClient.request('GET', news_url)
    #request = urllib2.Request( 'http://3g.163.com/touch/article/list/BBM54PGAwangning/0-10.html')
    # response是HTTPResponse对象
    response = httpClient.getresponse()
    translateResult = response.read()
    translateResult = translateResult.replace('artiList(','').replace(')','')
    jsonResult = json.loads(translateResult)

    if 'BBM54PGAwangning' in jsonResult:
        newses = jsonResult['BBM54PGAwangning']
        articles = []
        for news in newses:
            article = {}
            article['title'] = news['title']
            article['description'] = news['digest']
            article['picurl'] = news['imgsrc']
            article['url'] = news['url']
            articles.append(article)
    print articles
    return articles

#getNews(u'头条新闻')