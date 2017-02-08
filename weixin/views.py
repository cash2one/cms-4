
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import chardet
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from wechat_sdk.messages import VoiceMessage
from mezzanine.blog.models import BlogPost, BlogCategory
import sys
import fanyi
import news
import jiqiren

reload(sys)
sys.setdefaultencoding('utf8')

WECHAT_TOKEN = 'yuxuanyixiao'
AppID = 'wx6c1c0226980f62e2'
AppSecret = '5b29cdb78ab3cdd95972d7a9bee4cd24'

welcomeTitle = '欢迎关注公众号，点击查看我们的详细功能'
logoUrl = 'http://mmbiz.qlogo.cn/mmbiz_jpg/WOBRP1ClHtJ94zJYlan7fW8ZWrSmxY6eYvf96Ricm5ToBbpib3Kia5R5yZmKia38sqzP7BJDmeeGLYY2Xrj4ZU9icpA/0?wx_fmt=jpeg'
welcomeDescription = ('''
我们非常聪明的机器人可以回答你很多问题啦～\n
想听笑话，试试给我说 “讲个笑话呗”\n
想查天气，试试给我说“苏州今天天气怎么样”\n
想看新闻，试试给我说“刘德华的新闻”\n
想做新菜，试试给我说 “回锅肉”\n
想查快递，试试告诉我 “顺丰＋ 快递号”\n\n
欢迎大家使用，更多功能正在开发中，敬请期待！\n
请将宝贵意见发给我们.
''')
detailUrl = ''

# 实例化 WechatBasic

wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)

 

@csrf_exempt

def weixin_main(request):
    reply_text = ''
    content = ''
    fromUser = ''
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")

    # 解析本次请求的 XML 数据

    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()
    fromUser = message.source
    print  'fromUser : ', fromUser
    # 关注事件以及不匹配时的默认回复
    # response = wechat_instance.response_text(
    #     content = (
    #         '感谢您的关注！\n回复【功能】两个字查看支持的功能，还可以回复任意内容进行中英翻译[支持语音识别]\n'
    #         '1. 回复【资讯】可以推送相关资讯.\n'
    #         '2.回复新闻【头条新闻】【娱乐新闻】【科技新闻】【军事新闻】【财经新闻】【体育新闻】获取热门新闻'
    #         '3.回复任意中英文词语，可以进行中英翻译[支持语音识别]\n'
    #         '还有更多功能正在开发中哦，尽情期待，请将宝贵建议发送给我 ^_^\n'
    #         '【<a href="http://www.pyuxuan.cn">轩轩一笑</a>】'
    #        ))
    welcomeArticles = []
    welcomeArticle = {}
    welcomeArticle['title'] = welcomeTitle
    welcomeArticle['description'] = welcomeDescription
    welcomeArticle['picurl'] = logoUrl
    welcomeArticle['url'] = None
    welcomeArticles.append(welcomeArticle)
    response = wechat_instance.response_news(welcomeArticles)

    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.strip()
    elif isinstance(message, VoiceMessage):  
        reply_text = '语音内容:\n'
        print 'message.recognition : ',message.recognition
        if message.recognition is None:
           reply_text = reply_text + '内容为空'
        else:
           content = message.recognition.strip()
           reply_text = reply_text + content + '\n'
           # print chardet.detect(content)
           # content = content.replace('160','')
           # print content.decode("ascii").encode("utf-8")

           # reply_text = reply_text + '\n翻译结果:\n'
           # reply_text = reply_text + fanyi.baidu_translate(content,'auto','en')
        # print reply_text
        # response = wechat_instance.response_text(content=reply_text)

    if content == '功能':
        reply_text = (
            '目前支持的功能：\n1. 回复【资讯】可以推送相关资讯.\n'
            '2.回复新闻【头条新闻】【娱乐新闻】【科技新闻】【军事新闻】【财经新闻】【体育新闻】获取热门新闻'
            '3.回复任意中英文词语，可以进行中英翻译[支持语音识别]\n'
            '还有更多功能正在开发中哦，尽情期待，请将宝贵建议发送给我 ^_^\n'
            '【<a href="http://www.pyuxuan.cn">轩轩一笑</a>】'
        )
        print reply_text
        response = wechat_instance.response_text(content=reply_text)
    # elif content.endswith('资讯'):
    #     blog_posts = BlogPost.objects.published(for_user=None)[:10]
    #     var = 0;
    #     reply_text = '';
    #     for blog_post in blog_posts:
    #         print  blog_post.get_absolute_url()
    #         print blog_post.title
    #         print blog_post.content
    #         var = var + 1;
    #         reply_text += u'%d.【<a href="http://www.pyuxuan.cn%s">%s</a>】\n' % (
    #         var, blog_post.get_absolute_url(), blog_post.title)
    #     print reply_text
    #     response = wechat_instance.response_text(content=reply_text)
    elif content.find('新闻') > -1:
        result = jiqiren.getAnswerByAI(content, fromUser, 'GET')
        if result is not None:
            responseType = result['responseType']
            if responseType == 'article':
                articles = result['content']
                response = wechat_instance.response_news(articles)
            else :
                articles = news.getNews(content)
                response = wechat_instance.response_news(articles)
        else :
            articles = news.getNews(content)
            response = wechat_instance.response_news(articles)

    # elif content <> '':
    #     reply_text = reply_text + '翻译结果:\n'
    #     reply_text = reply_text + fanyi.baidu_translate(content, 'auto', 'en')
    #     print reply_text
    #     response = wechat_instance.response_text(content=reply_text)
    else :
        # 调用智能机器人回答问题，解析分析答案返回微信客户端
        result = jiqiren.getAnswerByAI(content, fromUser, 'GET')
        if result is not None :
            responseType = result['responseType']
            if responseType == 'text' :
                contentStr = result['content']
                response = wechat_instance.response_text(content=contentStr)
            elif responseType == 'url':
                contentStr = result['content']
                contentUrl = result['url']
                contentStr = contentStr + '【<a href="' + contentUrl + '">点击</a>】'
                response = wechat_instance.response_text(content=contentStr)
            elif responseType == 'article':
                articles = result['content']
                response = wechat_instance.response_news(articles)
    print response
    return HttpResponse(response, content_type="application/xml")
