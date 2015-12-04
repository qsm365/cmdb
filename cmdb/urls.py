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
from openstack.views import *

baseurl="^cmdb"

urlpatterns = [
    
    url(baseurl+'[/]?$',home),
    url(baseurl+'/login[/]?$',login),
    url(baseurl+'/logout[/]?$',logout),
    url(baseurl+'/captcha[/]?$',captcha),
    
    
    url(baseurl+'/collector[/]?$',collector),
    
    url(baseurl+'/host[/]?(\d{1,11})?$',hosts),
    url(baseurl+'/host/group/(?P<groupid>\d{1,11})?$',hosts),
    url(baseurl+'/host/find$',host_find_json),
    
    url(baseurl+'/group[/]?(\d{1,11})?$',groups),
    url(baseurl+'/group/type/(?P<grouptype>host|config)?$',groups),
    url(baseurl+'/relationship/(add|remove)$',relationship),
    url(baseurl+'/relationship/(add|remove)/(single2single|group2single|single2group|group2group)$',relationship),
    url(baseurl+'/group/parameter/(add|remove)$',parameters),
    url(baseurl+'/group/new$',new_group),
    url(baseurl+'/group/edit/(\d{1,11})$',edit_group),
    
    url(baseurl+'/config[/]?(\d{1,11})?$',configs),
    url(baseurl+'/config/group/(?P<groupid>\d{1,11})?$',configs),
    url(baseurl+'/config/new$',new_config),
    url(baseurl+'/config/edit/(\d{1,11})$',edit_config),
    url(baseurl+'/config/find$',config_find_json),
    
    url(baseurl+'/parameter/find$',parameter_find_json),
    
    url(baseurl+'/report[/]?(\d{1,11})?$',reports),
    url(baseurl+'/report/group/(?P<groupid>\d{1,11})?$',reports),
    
    url(baseurl+'/enc$',externalNodeClassifier),
    url(baseurl+'/importreport$',importReport),
    
    url(baseurl+'/container/update$',container_update),
    
    url(baseurl+'/application[/]?(\d{1,11})?$',applications),
    url(baseurl+'/application/new[/]?$',new_application),
    url(baseurl+'/application/new/create$',create_application),
    url(baseurl+'/application/new/detect$',detect_application),
    url(baseurl+'/application/edit/(\d{1,11})$',edit_application),
    url(baseurl+'/application/ping$',ping_docker),
    url(baseurl+'/application/containers',list_containers),
    
    url(baseurl+'/image[/]?(\d{1,11})?$',images),
    url(baseurl+'/image/new$',new_image),
    url(baseurl+'/image/ping$',ping_registry),
    url(baseurl+'/image/tags',list_images),
    
    url(baseurl+'/nova[/]?(\d{1,11})?$',nova),
    url(baseurl+'/hypervisor[/]?(\d{1,11})?$',hypervisor),
    url(baseurl+'/cinder[/]?(\d{1,11})?$',cinder),
    url(baseurl+'/glance[/]?(\d{1,11})?$',glance),
]
