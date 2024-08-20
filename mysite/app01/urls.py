 #coding=utf-8
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path as url
from django.urls import path
from app01 import views
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = [
    url(r'^index/$',views.index),           #主页
    url(r'^login/$',views.login),           #登录
    url(r'^logout/$',views.logout),         #注销
    url(r'^account/$',views.account),       #账户信息
    url(r'^account/change_password/$',views.show_change_password),  #修改密码页面
    url(r'^account/changepassword/$',views.change_password),        #修改密码
    url(r'^$',views.index),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)