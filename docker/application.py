from docker.models import APPLICATION
from core.models import Host,Resource

def create(name,description,createby):
    return

def show(appid):
    app=APPLICATION.objects.filter(id=appid)
    if app:
        return app

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

def delete(configid):
    apps=APPLICATION.objects.filter(id=configid)
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