#!usr/bin/env python  
# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^search/$', views.search, name='search'),
]