"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from core.views import *
from puppet.views import *
from mydocker.views import *

urlpatterns = [
    
    url('^cmdb[/]?$',home),
    url('^cmdb/login[/]?$',login),
    url('^cmdb/logout[/]?$',logout),
    url('^cmdb/captcha[/]?$',captcha),
    
    
    url('^cmdb/collector[/]?$',collector),
    
    url('^cmdb/host[/]?(\d{1,11})?$',hosts),
    url('^cmdb/host/group/(?P<groupid>\d{1,11})?$',hosts),
    url('^cmdb/host/find$',host_find_json),
    
    url('^cmdb/group[/]?(\d{1,11})?$',groups),
    url('^cmdb/group/type/(?P<grouptype>host|config)?$',groups),
    url('^cmdb/relationship/(add|remove)$',relationship),
    url('^cmdb/relationship/(add|remove)/(single2single|group2single|single2group|group2group)$',relationship),
    url('^cmdb/group/parameter/(add|remove)$',parameters),
    url('^cmdb/group/new$',new_group),
    url('^cmdb/group/edit/(\d{1,11})$',edit_group),
    
    url('^cmdb/config[/]?(\d{1,11})?$',configs),
    url('^cmdb/config/group/(?P<groupid>\d{1,11})?$',configs),
    url('^cmdb/config/new$',new_config),
    url('^cmdb/config/edit/(\d{1,11})$',edit_config),
    url('^cmdb/config/find$',config_find_json),
    
    url('^cmdb/parameter/find$',parameter_find_json),
    
    url('^cmdb/report[/]?(\d{1,11})?$',reports),
    url('^cmdb/report/group/(?P<groupid>\d{1,11})?$',reports),
    
    url('^cmdb/enc$',externalNodeClassifier),
    url('^cmdb/importreport$',importReport),
    
    url('^cmdb/application[/]?(\d{1,11})?$',applications),
    url('^cmdb/application/new[/]?$',new_application),
    url('^cmdb/application/new/create$',create_application),
    url('^cmdb/application/new/detect$',detect_application),
    url('^cmdb/application/edit/(\d{1,11})$',edit_application),
    url('^cmdb/application/ping$',ping_docker),
    url('^cmdb/application/containers',list_containers),
    
    url('^cmdb/image[/]?(\d{1,11})?$',images),
    url('^cmdb/image/new$',new_image),
    url('^cmdb/image/ping$',ping_registry),
    url('^cmdb/image/tags',list_images)
]
