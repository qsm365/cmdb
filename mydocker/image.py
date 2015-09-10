from mydocker.models import IMAGE
from core.models import Host,Resource

def create(repository,tag):
    return

def show(imgid):
    img=IMAGE.objects.filter(id=imgid)
    if img:
        return img

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