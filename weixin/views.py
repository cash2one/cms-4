
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
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

reload(sys)
sys.setdefaultencoding('utf8')

WECHAT_TOKEN = 'yuxuanyixiao'
AppID = 'wx6c1c0226980f62e2'
AppSecret = '5b29cdb78ab3cdd95972d7a9bee4cd24'

 

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
    # 关注事件以及不匹配时的默认回复
    response = wechat_instance.response_text(
        content = (
            '感谢您的关注！\n回复【功能】两个字查看支持的功能，还可以回复任意内容进行中英翻译[支持语音识别]\n'
            '1. 回复【资讯】可以推送相关资讯.\n'
            '2.回复新闻【头条新闻】【娱乐新闻】【科技新闻】【军事新闻】【财经新闻】【体育新闻】获取热门新闻'
            '3.回复任意中英文词语，可以进行中英翻译[支持语音识别]\n'
            '还有更多功能正在开发中哦，尽情期待，请将宝贵建议发送给我 ^_^\n'
            '【<a href="http://www.pyuxuan.cn">轩轩一笑</a>】'
           ))

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
           print content
           content.replace('。','')

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
    elif content.endswith('资讯'):
        blog_posts = BlogPost.objects.published(for_user=None)[:10]
        var = 0;
        reply_text = '';
        for blog_post in blog_posts:
            print  blog_post.get_absolute_url()
            print blog_post.title
            print blog_post.content
            var = var + 1;
            reply_text += u'%d.【<a href="http://www.pyuxuan.cn%s">%s</a>】\n' % (
            var, blog_post.get_absolute_url(), blog_post.title)
        print reply_text
        response = wechat_instance.response_text(content=reply_text)
    elif content.find('新闻') > -1:
        articles = news.getNews(content)
        response = wechat_instance.response_news(articles)
    elif content <> '':
        reply_text = reply_text + '翻译结果:\n'
        reply_text = reply_text + fanyi.baidu_translate(content, 'auto', 'en')
        print reply_text
        response = wechat_instance.response_text(content=reply_text)

    print response
    return HttpResponse(response, content_type="application/xml")
