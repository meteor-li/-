#!usr/bin/env python  
# -*- coding:utf-8 -*-
from django.conf.urls import url
from .views import Login,check_login,user,contact_list,sendmsg,getmsg
urlpatterns = [
    url(r'^Login.html$', Login),
    url(r'^check-login.html$', check_login),
    url(r'^user.html$', user),
    url(r'^contact-list.html$', contact_list),
    url(r'^sendmsg.html$',sendmsg),
    url(r'^getmsg.html$', getmsg)
]