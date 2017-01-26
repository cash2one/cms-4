from django.conf.urls import include, url
from . import views
urlpatterns = []
urlpatterns += [
                url(r'^wechat/$', views.weixin_main, name='wechat'),
]
