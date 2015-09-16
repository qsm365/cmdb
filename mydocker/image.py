from mydocker.models import IMAGE,APPLICATION
from core.models import Host,Resource
from mydocker import dockerclient

def create(registry_ip,registry_port,repository,tag,image_id):
    imageinfo=dockerclient.showRegistryImage(registry_ip, registry_port, image_id)
    print imageinfo['Size']
    img=IMAGE()
    img.imageid=image_id
    img.repository=repository
    img.tag=tag
    img.virtualsize=imageinfo['Size']
    img.created=imageinfo['created']
    img.registryip=registry_ip
    img.registryport=registry_port
    img.save()
    return

def show(imgid):
    img=IMAGE.objects.filter(id=imgid)
    if img:
        return img.first()

def showAll():
    re=IMAGE.objects.all()
    return re

def search(q):
    imgs=IMAGE.objects.filter(repository__icontains=q)
    re=[]
    if imgs:
        re= imgs.all()
    return re

def delete(imgid):
    imgs=IMAGE.objects.filter(id=imgid)
    if imgs:
        img=imgs.first()
        img.delete()
        
def getAppByImage(imgid):
    imgs=IMAGE.objects.filter(id=imgid)
    if imgs:
        img=imgs.first()
        imageid=img.imageid
        apps=APPLICATION.objects.filter(image=imageid).all()
        if apps:
            result=[]
            for app in apps:
                result.append(app.engineip)
            return result