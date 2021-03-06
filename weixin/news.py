#/usr/bin/env python
#coding=utf8
import httplib
import random
import urllib
import urllib2
import json

news_types = {
u"推荐新闻":{'url':"/touch/article/list/BA8J7DG9wangning/%d-%d.html",'keywords':'BA8J7DG9wangning'},
u"头条新闻":{'url':"/touch/article/list/BBM54PGAwangning/%d-%d.html",'keywords':'BBM54PGAwangning'},
u"娱乐新闻":{'url':"/touch/article/list/BA10TA81wangning/%d-%d.html",'keywords':'BA10TA81wangning'},
u"科技新闻":{'url':"/touch/article/list/BA8D4A3Rwangning/%d-%d.html",'keywords':'BA8D4A3Rwangning'},
u"军事新闻":{'url':"/touch/article/list/BAI67OGGwangning/%d-%d.html",'keywords':'BAI67OGGwangning'},
u"财经新闻":{'url':"/touch/article/list/BA8EE5GMwangning/%d-%d.html",'keywords':'BA8EE5GMwangning'},
u"时尚新闻":{'url':"/touch/article/list/BA8F6ICNwangning/%d-%d.html",'keywords':'BA8F6ICNwangning'},
u"体育新闻":{'url':"/touch/article/list/BA8E6OEOwangning/%d-%d.html",'keywords':'BA8E6OEOwangning'},
u"手机新闻":{'url':"/touch/article/list/BAI6I0O5wangning/%d-%d.html",'keywords':'BAI6I0O5wangning'},
u"游戏新闻":{'url':"/touch/article/list/BAI6RHDKwangning/%d-%d.html",'keywords':'BAI6RHDKwangning'},
u"数码新闻":{'url':"/touch/article/list/BAI6JOD9wangning/%d-%d.html",'keywords':'BAI6JOD9wangning'},
u"教育新闻":{'url':"/touch/article/list/BA8FF5PRwangning/%d-%d.html",'keywords':'BA8FF5PRwangning'},
u"健康新闻":{'url':"/touch/article/list/BDC4QSV3wangning/%d-%d.html",'keywords':'BDC4QSV3wangning'},
u"汽车新闻":{'url':"/touch/article/list/BA8DOPCSwangning/%d-%d.html",'keywords':'BA8DOPCSwangning'},
u"家居新闻":{'url':"/touch/article/list/BAI6P3NDwangning/%d-%d.html",'keywords':'BAI6P3NDwangning'},
u"房产新闻":{'url':"/touch/article/list/BAI6MTODwangning/%d-%d.html",'keywords':'BAI6MTODwangning'},
u"旅游新闻":{'url':"/touch/article/list/BEO4GINLwangning/%d-%d.html",'keywords':'BEO4GINLwangning'},
u"亲子新闻":{'url':"/touch/article/list/BEO4PONRwangning/%d-%d.html",'keywords':'BEO4PONRwangning'}
}

def getNews(news_type) :
    print 'news_type :', news_type
    if news_type not in news_types :
        news_type = u"推荐新闻"
    news_dict = news_types[news_type]
    news_url = news_dict['url']
    news_keywords = news_dict['keywords']
    seq = random.randint(0,50)
    news_url = news_url % (seq,5)
    httpClient = httplib.HTTPConnection('3g.163.com')
    httpClient.request('GET', news_url)
    #request = urllib2.Request( 'http://3g.163.com/touch/article/list/BBM54PGAwangning/0-10.html')
    # response是HTTPResponse对象
    response = httpClient.getresponse()
    translateResult = response.read()
    translateResult = translateResult.replace('artiList(','').replace(')','')
    jsonResult = json.loads(translateResult)

    if news_keywords in jsonResult:
        newses = jsonResult[news_keywords]
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
    else :
        return None

#getNews(u'头条新闻')