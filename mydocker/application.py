from mydocker.models import APPLICATION
from core.models import Host,Resource
import dockerclient

def create_new():
    return

def create_detect(host_id,engine_ip,engine_port,container_id,app_name,app_desc):
    containerinfo=dockerclient.detect(engine_ip, engine_port, container_id)
    #print containerinfo
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
        #print "1"
        hosts=Host.objects.filter(id=host_id)
        if hosts:
            host=hosts.first()
            res=Resource()
            res.type="application"
            res.host=host
            res.resource_id=app.id
            res.save()
            #print "2"

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