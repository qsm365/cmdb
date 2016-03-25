from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
import nova

# Create your views here.
def vm(request,vmid=0):
    if not vmid:
        context={}
        p=int(request.GET.get('page',1))
        re=nova.listInstances()
        context['title']="Nova VM List"
        if re:
            page=Paginator(re,10)
            if p>0 and p<=page.num_pages:
                context['page']=page.page(p)
            else:
                context['page']=page.page(1)
            context['num_pages']=page.num_pages
            for pa in context['page']:
                pa['url']="/cmdb/nova/"+str(pa['id'])
        context['uri']='nova'
        context['with_group']=True
        context['with_new']=True
        context['nosearch']=True
        return render(request, 'list.html',context)
    else:
        if request.method=='POST':
            return HttpResponse("ok")
        else:
            re=nova.showInstances(vmid)
            if re:
                context=re
                context['title']="VM Instance Info"
                context['vm']=re
                return render(request, 'openstack/vm.html',context)
            else:
                return HttpResponseRedirect("/cmdb/nova")

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
            return render(request, 'openstack/hypervisor.html',context)

def volume(request,volid=0):
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
            return render(request, 'openstack/cinder.html',context)
    
def image(request,imgid=0):
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
            return render(request, 'openstack/glance.html',context)