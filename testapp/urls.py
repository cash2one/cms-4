from django.conf.urls import include, url
from . import views
urlpatterns = []
urlpatterns += [
                url(r'^$', views.weixin_main, name='wechat'),
]
