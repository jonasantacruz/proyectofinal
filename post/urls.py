from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    )

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create, name='news'),
    url(r'^(?P<id>\d+)/$', post_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', post_update, name = 'update'),
    url(r'^(?P<id>\d+)/delete/$', post_delete),
    #url(r'^$', login,{'template_name':'index.html'}, name='login'),
    #url(r'^post/$', <appname>.views.<function_name>"),
]
