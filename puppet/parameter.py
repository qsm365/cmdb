from core.models import Resource,Host,Group,IP
from puppet.models import PARAMETER

def createByHost(hostid,key,value):
    hosts=Host.objects.filter(id=hostid)
    if hosts:
        host=hosts.first()
        
        para=PARAMETER()
        para.key=key
        para.value=value
        para.save()
        
        res=Resource()
        res.name="params"
        res.type="parameter"
        res.resource_id=para.id
        res.host=host
        res.save()
        
        return para.id

def createByGroup(groupid,key,value):
    group=Group.objects.filter(id=groupid)
    if group:
        hosts=Host.objects.filter(group=group).all()
        if hosts:
            for host in hosts:
                para=PARAMETER()
                para.key=key
                para.value=value
                para.save()
                res=Resource()
                res.name="params"
                res.type="parameter"
                res.resource_id=para.id
                res.host=host
                res.save()

def delete(pid):
    paras=PARAMETER.objects.filter(id=pid)
    if paras:
        para=paras.first()
        res=Resource.objects.filter(type='parameter',resource_id=para.id)
        if res:
            r=res.first()
            r.delete()
        para.delete()

def listByHost(hostid):
    hosts=Host.objects.filter(id=hostid)
    if hosts:
        host=hosts.first()
        res=Resource.objects.filter(host=host,type="parameter")
        if res:
            re=set()
            for r in res:
                para=PARAMETER.objects.filter(id=r.resource_id)
                if para:
                    re.add(para.first())
            return re

def listByGroup(groupid):
    groups=Group.objects.filter(id=groupid)
    if groups:
        group=groups.first()
        hosts=Host.objects.filter(group=group).all()
        if hosts:
            re={}
            for host in hosts:
                r=[]
                res=Resource.objects.filter(host=host,type="parameter")
                if res:
                    for rs in res:
                        para=PARAMETER.objects.filter(id=rs.resource_id)
                        if para:
                            r.append(para.first())
                if r:
                    res=Resource.objects.filter(host=host,type="ip")
                    if res:
                        ip=IP.objects.filter(id=res.first().resource_id).first()
                        re[ip.ipv4]=r
            return re