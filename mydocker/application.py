from mydocker.models import APPLICATION
from core.models import Host,Resource,IP
import dockerclient

def create_new(engine_ip,engine_port,host_id,name,description,imagename,command,entrypoint,container_name,host_name,network_mode,privileged,security_opt,ulimit_nofile,ulimit_noproc,ports,port_bindings,volume,binds,dns_server,hosts,environment):
    containerinfo=dockerclient.create(engine_ip, engine_port, imagename,command,entrypoint,container_name,host_name,network_mode,privileged,security_opt,ulimit_nofile,ulimit_noproc,ports,port_bindings,volume,binds,dns_server,hosts,environment)
    if containerinfo:
        app=APPLICATION()
        app.name=name
        app.description=description
        app.containerid=containerinfo['container_id']
        app.containername=containerinfo['container_name']
        app.image=containerinfo['image']
        app.created=containerinfo['created']
        app.status=containerinfo['status']
        app.engineip=engine_ip
        app.engineport=engine_port
        app.save()
        hosts=Host.objects.filter(id=host_id)
        if hosts:
            host=hosts.first()
            res=Resource()
            res.type="application"
            res.host=host
            res.resource_id=app.id
            res.save()
        return "create success"
    return "create failed:"+str(containerinfo['msg'])

def create_detect(host_id,engine_ip,engine_port,container_id,app_name,app_desc):
    containerinfo=dockerclient.detect(engine_ip, engine_port, container_id)
    if containerinfo:
        app=APPLICATION()
        app.name=app_name
        app.description=app_desc
        app.containerid=container_id
        app.containername=containerinfo['container_name']
        app.image=containerinfo['image']
        app.created=containerinfo['created']
        app.status=containerinfo['status']
        app.engineip=engine_ip
        app.engineport=engine_port
        app.save()
        hosts=Host.objects.filter(id=host_id)
        if hosts:
            host=hosts.first()
            res=Resource()
            res.type="application"
            res.host=host
            res.resource_id=app.id
            res.save()

def show(appid):
    app=APPLICATION.objects.filter(id=appid)
    if app:
        return app.first()

def showAll():
    re=APPLICATION.objects.all()
    return re

def search(q):
    apps=APPLICATION.objects.filter(name__icontains=q) | APPLICATION.objects.filter(containername__icontains=q)
    re=[]
    if apps:
        re= apps.all()
    return re

def listByHost(hostid):
    hosts=Host.objects.filter(id=hostid)
    if hosts:
        re=[]
        host=hosts.first()
        reses=Resource.objects.filter(host=host,type='application').order_by('-id').all()
        for res in reses:
            app=APPLICATION.objects.filter(id=res.resource_id).first()
            re.append(app)
        return re

def listByIp(ip):
    re=APPLICATION.objects.filter(engineip=ip)
    if re:
        return re.all()

def delete(appid):
    apps=APPLICATION.objects.filter(id=appid)
    if apps:
        app=apps.first()
        app.delete()
        
def edit(appid,name,description):
    apps=APPLICATION.objects.filter(id=appid)
    if apps:
        app=apps.first()
        app.name=name
        app.description=description
        app.save()

def exist(containerid):
    re=APPLICATION.objects.filter(containerid=containerid)
    if re:
        return True
    return False

def updateStatus(app):
    app.status=dockerclient.updateContainerStatus(app.engineip, app.engineport, app.containerid)
    app.save()
    
def auto_detect(engine_ip,engine_port,container_id):
    ip=IP.objects.filter(ipv4__contains=engine_ip)
    if ip:
        containerinfo=dockerclient.detect(engine_ip, engine_port, container_id)
        if containerinfo:
            app=APPLICATION()
            app.name="[auto detect]"+containerinfo['container_name']
            app.description="[auto detect]"+str(containerinfo['container_name'])
            app.containerid=container_id
            app.containername=containerinfo['container_name']
            app.image=containerinfo['image']
            app.created=containerinfo['created']
            app.status=containerinfo['status']
            app.engineip=engine_ip
            app.engineport=engine_port
            app.save()
            i=ip.first()
            res=Resource.objects.filter(type='ip',resource_id=i.id)
            host=res.first().host
            res=Resource()
            res.type="application"
            res.host=host
            res.resource_id=app.id
            res.save()