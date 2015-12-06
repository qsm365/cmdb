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
from django.conf.urls import url
#from django.contrib import admin
import core.views
import puppet.views
import mydocker.views
import openstack.views

baseurl="^cmdb"

urlpatterns = [
    
    url(baseurl+'[/]?$',core.views.home),
    url(baseurl+'/login[/]?$',core.views.login),
    url(baseurl+'/logout[/]?$',core.views.logout),
    url(baseurl+'/captcha[/]?$',core.views.captcha),
    
    
    url(baseurl+'/collector[/]?$',core.views.collector),
    
    url(baseurl+'/host[/]?(\d{1,11})?$',core.views.hosts),
    url(baseurl+'/host/group/(?P<groupid>\d{1,11})?$',core.views.hosts),
    url(baseurl+'/host/find$',core.views.host_find_json),
    
    url(baseurl+'/group[/]?(\d{1,11})?$',core.views.groups),
    url(baseurl+'/group/type/(?P<grouptype>host|config)?$',core.views.groups),
    url(baseurl+'/relationship/(add|remove)$',core.views.relationship),
    url(baseurl+'/relationship/(add|remove)/(single2single|group2single|single2group|group2group)$',core.views.relationship),
    url(baseurl+'/group/parameter/(add|remove)$',puppet.views.parameters),
    url(baseurl+'/group/new$',core.views.new_group),
    url(baseurl+'/group/edit/(\d{1,11})$',core.views.edit_group),
    
    url(baseurl+'/config[/]?(\d{1,11})?$',puppet.views.configs),
    url(baseurl+'/config/group/(?P<groupid>\d{1,11})?$',puppet.views.configs),
    url(baseurl+'/config/new$',puppet.views.new_config),
    url(baseurl+'/config/edit/(\d{1,11})$',puppet.views.edit_config),
    url(baseurl+'/config/find$',puppet.views.config_find_json),
    
    url(baseurl+'/parameter/find$',puppet.views.parameter_find_json),
    
    url(baseurl+'/report[/]?(\d{1,11})?$',puppet.views.reports),
    url(baseurl+'/report/group/(?P<groupid>\d{1,11})?$',puppet.views.reports),
    
    url(baseurl+'/enc$',puppet.views.externalNodeClassifier),
    url(baseurl+'/importreport$',puppet.views.importReport),
    
    url(baseurl+'/container/update$',mydocker.views.container_update),
    
    url(baseurl+'/application[/]?(\d{1,11})?$',mydocker.views.applications),
    url(baseurl+'/application/new[/]?$',mydocker.views.new_application),
    url(baseurl+'/application/new/create$',mydocker.views.create_application),
    url(baseurl+'/application/new/detect$',mydocker.views.detect_application),
    url(baseurl+'/application/edit/(\d{1,11})$',mydocker.views.edit_application),
    url(baseurl+'/application/ping$',mydocker.views.ping_docker),
    url(baseurl+'/application/containers',mydocker.views.list_containers),
    
    url(baseurl+'/image[/]?(\d{1,11})?$',mydocker.views.images),
    url(baseurl+'/image/new$',mydocker.views.new_image),
    url(baseurl+'/image/ping$',mydocker.views.ping_registry),
    url(baseurl+'/image/tags',mydocker.views.list_images),
    
    url(baseurl+'/nova[/]?(\d{1,11})?$',openstack.views.nova),
    url(baseurl+'/hypervisor[/]?(\d{1,11})?$',openstack.views.hypervisor),
    url(baseurl+'/cinder[/]?(\d{1,11})?$',openstack.views.cinder),
    url(baseurl+'/glance[/]?(\d{1,11})?$',openstack.views.glance),
]
