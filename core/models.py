from django.db import models

# Create your models here.

class Group(models.Model):
    name=models.CharField(max_length=30)
    type=models.CharField(max_length=30,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    url=""
    def __str__(self):
        return self.name
    def setUrl(self,url):
        self.url=url

class Host(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    group=models.ManyToManyField(Group)
    ip=""
    url=""
    def __str__(self):
        return self.name
    def setIP(self,ip):
        self.ip=ip
    def setUrl(self,url):
        self.url=url
    
class Resource(models.Model):
    name=models.CharField(max_length=255,null=True)
    type=models.CharField(max_length=30,null=True)
    resource_id=models.IntegerField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    host=models.ForeignKey(Host,null=True)
    def __str__(self):
        return self.name

class IP(models.Model):
    ipv4=models.CharField(max_length=20)
    def __str__(self):
        return self.ipv4
    
class OS(models.Model):
    operatingsystem=models.CharField(max_length=30)
    operatingsystemrelease=models.CharField(max_length=255)
    kernel=models.CharField(max_length=30)
    kernelversion=models.CharField(max_length=255)
    def __str__(self):
        return self.osfamily+"-"+self.version
    
class HARDWARE(models.Model):
    architecture=models.CharField(max_length=30)
    processortype=models.CharField(max_length=255)
    processorcount=models.IntegerField()
    memorytotal=models.CharField(max_length=30)
    uniqueid=models.CharField(max_length=50)
    is_virtual=models.BooleanField()
    def __str__(self):
        return self.architecture+"with:"+str(self.processorcount)+"CPU;"+self.memorytotal+"MEM"
    
class USER(models.Model):
    name=models.CharField(max_length=100)
    group=models.CharField(max_length=100)
    locked=models.BooleanField()
    def __str__(self):
        return self.name