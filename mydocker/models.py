from django.db import models

# Create your models here.
class APPLICATION(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(null=True)
    containerid=models.CharField(max_length=100)
    containername=models.CharField(max_length=100)
    image=models.CharField(max_length=100)
    created=models.DateTimeField()
    status=models.CharField(max_length=30)
    engineip=models.CharField(max_length=30)
    engineport=models.CharField(max_length=10)
    url=""
    def __str__(self):
        return self.name
    def setUrl(self,url):
        self.url=url
    
class IMAGE(models.Model):
    imageid=models.CharField(max_length=100)
    repository=models.CharField(max_length=30)
    tag=models.CharField(max_length=30)
    virtualsize=models.BigIntegerField()
    created=models.DateTimeField()
    registryip=models.CharField(max_length=30)
    registryport=models.CharField(max_length=10)
    url=""
    def __str__(self):
        return self.imageid
    def setUrl(self,url):
        self.url=url