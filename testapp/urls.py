from django.conf.urls import include, url
from . import views

urlpatterns += [
                url(r'^wechat/$', views.weixin_main, name='wechat'),
]
