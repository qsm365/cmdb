from django.db import models
from core.models import Group

# Create your models here.
class CONFIG(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(null=True)
    classname=models.CharField(max_length=100)
    group=models.ManyToManyField(Group)
    url=""
    def __str__(self):
        return self.name
    def setUrl(self,url):
        self.url=url

class PARAMETER(models.Model):
    key=models.CharField(max_length=30)
    value=models.CharField(max_length=30)
    def __str__(self):
        return self.key+"="+self.value

class PPREPORT(models.Model):
    status=models.CharField(max_length=30)
    time=models.DateTimeField()
    version=models.CharField(max_length=50)
    url=""
    name=""
    def setUrl(self,url):
        self.url=url
    def setHost(self,name):
        self.name=name

class PPMETRICS(models.Model):
    category=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    value=models.DecimalField(max_digits=12,decimal_places=6)
    report=models.ForeignKey(PPREPORT,null=True)

class PPREPORTLOG(models.Model):
    level=models.CharField(max_length=255)
    message=models.TextField()
    time=models.DateTimeField()
    report=models.ForeignKey(PPREPORT,null=True)