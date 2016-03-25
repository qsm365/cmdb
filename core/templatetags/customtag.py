from django import template
from openstack import nova,glance

register = template.Library()

@register.filter
def lookup(d, key):
    return d.get(key, '')

@register.filter
def getFlavor(flavorId):
    return nova.getFlavor(flavorId)

@register.filter
def getImage(imageId):
    return glance.getImage(imageId)

@register.filter
def addUnit(value):
    l=len(str(value))
    if l>9:
        return str(value/1024/1024/1024)+"GB"
    elif l>6:
        return str(value/1024/1024)+"MB"
    elif l>3:
        return str(value/1024)+"KB"
    else:
        return str(value)+"B"