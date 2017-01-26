from django.conf.urls import include, url

urlpatterns = []

urlpatterns += [
                url(r'^wechat/$', views.weixin_main, name='wechat'),
]
