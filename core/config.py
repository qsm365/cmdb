from core.models import CONFIG,Host,Resource,Group
import os

def create(name,description,classname):
    conf=CONFIG()
    conf.name=name
    conf.description=description
    conf.classname=classname
    conf.save()
    return conf.id

def show(configid):
    confs=CONFIG.objects.filter(id=configid)
    if confs:
        return confs.first()
    
def list():
    re=CONFIG.objects.all()
    return re

def get(configid):
    c=CONFIG.objects.filter(id=configid)
    if c:
        return c.first()

def search(q):
    conf=CONFIG.objects.filter(name__icontains=q) | CONFIG.objects.filter(classname__icontains=q)
    re=[]
    if conf:
        re= conf.all()
    return re

def listByGroup(groupid):
    group=Group.objects.filter(id=groupid,type='CONFIG')
    if group:
        g=group.first()
        re=CONFIG.objects.filter(group=g).all()
        return re

def delete(configid):
    confs=CONFIG.objects.filter(id=configid)
    if confs:
        conf=confs.first()
        conf.delete()
        
def edit(configid,name,description,classname):
    confs=CONFIG.objects.filter(id=configid)
    if confs:
        conf=confs.first()
        conf.name=name
        conf.description=description
        conf.classname=classname
        conf.save()

def ppfile(configid):
    confs=CONFIG.objects.filter(id=configid)
    if confs:
        re={}
        conf=confs.first()
        classname=conf.classname
        for root,dirs,files in os.walk("/etc/puppet/modules/"+classname+"/manifests/"):
            for name in files:
                f=open(root+name)
                content=f.read()
                re[name]=content
        return re

def hostsWithConfig(configid):
    confs=CONFIG.objects.filter(id=configid)
    if confs:
        conf=confs.first()
        res=Resource.objects.filter(type="config",resource_id=conf.id).all()
	re=[]
	for r in res:
           re.append(r.host)
	return re
