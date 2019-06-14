"""myblog_03 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog.feeds import AllPostsRssFeed
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('app.urls')),
    url(r'', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'', include('comments.urls')),
    url(r'^all/rss/$', AllPostsRssFeed(), name='rss'),
# 其中namespace参数为我们指定了命名空间，这说明这个urls.py中的url是blog app下的，这样即使不同的app下有相同url也不会冲突了。
]
