from core.models import OS,HARDWARE,IP,Resource,Host,USER,Group
from puppet.models import PPREPORT,PPREPORTLOG,CONFIG,PARAMETER
from mydocker.models import APPLICATION

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def resolve(s):
    s=s.replace("\r","")
    co=s.split("\n")
    re={}
    for c in co:
        v=c.split("=")
        if len(v)>1:
            if len(v)>2:
                to=v[2].split(";")
                re['user']=[]
                for t in to:
                    if t:
                        r=t.split(":")
                        re['user'].append({'name':r[0],'group':r[1],'locked':r[2]}) 
            else:
                re[v[0]]=v[1]
    #print re
    return re

def exists(hostname,sip):
    host=Host.objects.filter(name=hostname).order_by('-created_at')
    if host:
        res=Resource.objects.filter(host=host.first(),type="ip")
        if res:
            ip=IP.objects.filter(id=res.first().resource_id).first().ipv4
            if ip==sip:
                return host.first().id
    return False
    
def create(s,sip):
    if len(s)==12:
        os=OS()
        os.operatingsystem=s['operatingsystem']
        os.operatingsystemrelease=s['operatingsystemrelease']
        os.kernel=s['kernel']
        os.kernelversion=s['kernelversion']
        os.save()
        
        hardware=HARDWARE()
        hardware.architecture=s['architecture']
        hardware.processortype=s['processortype']
        hardware.processorcount=s['processorcount']
        hardware.memorytotal=s['memorytotal']
        hardware.uniqueid=s['uniqueid']
        hardware.is_virtual=True if s['is_virtual']=='True' else False
        hardware.save()
        
        ip=IP()
        ip.ipv4=sip
        ip.save()
                
        host=Host()
        host.name=s['hostname']
        host.save()
                
        for u in s['user']:
            user=USER()
            user.name=u['name']
            user.group=u['group']
            user.locked=True if u['locked']=='true' else False
            user.save()
            
            res=Resource()
            res.name='User list'
            res.type='user'
            res.resource_id=user.id
            res.host=host
            res.save()
        
        res=Resource()
        res.name='OS'
        res.type='os'
        res.resource_id=os.id
        res.host=host
        res.save()
        
        res=Resource()
        res.name='Hardware'
        res.type='hardware'
        res.resource_id=hardware.id
        res.host=host
        res.save()
        
        res=Resource()
        res.name='IP Address'
        res.type='ip'
        res.resource_id=ip.id
        res.host=host
        res.save()

def update(hostid,s,sip):
    if len(s)==12:
        host=Host.objects.filter(id=hostid)
        if host:
            host=host.first()
            os_rid=Resource.objects.filter(host=host,type='os')
            hw_rid=Resource.objects.filter(host=host,type='hardware')
            user_rid=Resource.objects.filter(host=host,type='user')
            for rid in os_rid:
                OS.objects.filter(id=rid.resource_id).all().delete()
                rid.delete()
            for rid in hw_rid:
                HARDWARE.objects.filter(id=rid.resource_id).all().delete()
                rid.delete()
            for rid in user_rid:
                USER.objects.filter(id=rid.resource_id).all().delete()
                rid.delete()
            os=OS()
            os.operatingsystem=s['operatingsystem']
            os.operatingsystemrelease=s['operatingsystemrelease']
            os.kernel=s['kernel']
            os.kernelversion=s['kernelversion']
            os.save()
            
            res=Resource()
            res.name='OS'
            res.type='os'
            res.resource_id=os.id
            res.host=host
            res.save()
            
            hardware=HARDWARE()
            hardware.architecture=s['architecture']
            hardware.processortype=s['processortype']
            hardware.processorcount=s['processorcount']
            hardware.memorytotal=s['memorytotal']
            hardware.uniqueid=s['uniqueid']
            hardware.is_virtual=True if s['is_virtual']=='True' else False
            hardware.save()
            
            res=Resource()
            res.name='Hardware'
            res.type='hardware'
            res.resource_id=hardware.id
            res.host=host
            res.save()
            
            for u in s['user']:
                user=USER()
                user.name=u['name']
                user.group=u['group']
                user.locked=True if u['locked']=='true' else False
                user.save()
                
                res=Resource()
                res.name='User list'
                res.type='user'
                res.resource_id=user.id
                res.host=host
                res.save()
            
def delete(hostid):
    host=Host.objects.filter(id=hostid)
    if host:
        reses=Resource.objects.filter(host=host)
        if reses:
            for res in reses:
                if res.type!='config':
                    t=eval(res.type.upper()).objects.filter(id=res.resource_id)
                    if t:
                        t.first().delete()
                res.delete()
        host.first().delete()

def show(hostid):
    host=Host.objects.filter(id=hostid)
    if host:
        re={}
        re['host']=host.first()
        reses=Resource.objects.filter(host=host).exclude(type='report')
        for res in reses:
            t=eval(res.type.upper()).objects.filter(id=res.resource_id)
            if t:
                if type(re.get(res.type)) is dict:
                    re[res.type][res.id]=t.first()
                else:
                    re[res.type]={}
                    re[res.type][res.id]=t.first()
        reses=Resource.objects.filter(host=host,type='ppreport').order_by('-created_at')[:2]
        if reses:
            resource_id=reses.first().resource_id
            t=PPREPORT.objects.filter(id=resource_id)
            if t:
                ppreport=t.first()
                re['ppreport']=ppreport
                ppreportlog=PPREPORTLOG.objects.filter(report=ppreport).all()
                re['ppreportlog']=ppreportlog
        return re
    
def showAll():
    re=Host.objects.all()
    return re

def edit_desc(hostid,desc):
    host=Host.objects.filter(id=hostid)
    if host:
        h=host.first()
        h.description=desc
        h.save()

def get(hostid):
    h=Host.objects.filter(id=hostid)
    if h:
        return h.first()

def search(q):
    host=Host.objects.filter(name__icontains=q)
    re=[]
    if host:
        re= host.all()
    ip=IP.objects.filter(ipv4__contains=q)
    for i in ip:
        res=Resource.objects.filter(type='ip',resource_id=i.id)
        re.append(res.first().host)
    return re

def listByGroup(groupid):
    group=Group.objects.filter(id=groupid,type='Host')
    if group:
        g=group.first()
        re=Host.objects.filter(group=g).all()
        return re

def getIP(hostid):
    host=Host.objects.filter(id=hostid)
    if host:
        res=Resource.objects.filter(host=host.first(),type="ip")
        if res:
            ip=IP.objects.filter(id=res.first().resource_id).first()
            return ip.ipv4
        
def addConfig(h,c):
    if h and c:
        res=Resource()
        res.name='Config'
        res.type='config'
        res.resource_id=c.id
        res.host=h
        res.save()
        
def removeConfig(h,c):
    if h and c:
        res=Resource.objects.filter(host=h,type='config',resource_id=c.id).all()
        if res:
            res.delete()
