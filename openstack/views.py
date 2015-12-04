from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def nova(request,vmid=0):
    if not vmid:
        context={}
        context['title']="Nova VM List"
        context['uri']='nova'
        context['with_group']=True
        context['with_new']=True
        return render(request, 'list.html',context)
    else:
        if request.method=='POST':
            return HttpResponse("ok")
        else:
            context={}
            return render(request, 'nova.html',context)

def hypervisor(request,hvid=0):
    if not hvid:
        context={}
        context['title']="Nova Hypervisor List"
        context['uri']='nova'
        context['with_group']=True
        context['with_new']=True
        return render(request, 'list.html',context)
    else:
        if request.method=='POST':
            return HttpResponse("ok")
        else:
            context={}
            return render(request, 'nova.html',context)

def cinder(request,volid=0):
    if not volid:
        context={}
        context['title']="Cinder List"
        context['uri']='cinder'
        context['with_group']=False
        context['with_new']=True
        return render(request, 'list.html',context)
    else:
        if request.method=='POST':
            return HttpResponse("ok")
        else:
            context={}
            return render(request, 'cinder.html',context)
    
def glance(request,imgid=0):
    if not imgid:
        context={}
        context['title']="Glance List"
        context['uri']='glance'
        context['with_group']=False
        context['with_new']=True
        return render(request, 'list.html',context)
    else:
        if request.method=='POST':
            return HttpResponse("ok")
        else:
            context={}
            return render(request, 'glance.html',context)