from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mydocker import dockerclient,application
from django.core.paginator import Paginator

# Create your views here.
@login_required
def applications(request,appid=0):
    if not appid:
        context={}
        q=request.GET.get('q')
        p=int(request.GET.get('page',1))
        if q:
            re=application.search(q)
            context['title']="Applications in search"
        else:
            re=application.showAll()
            context['title']="Applications List"
        if re:
            page=Paginator(re,10)
            if p>0 and p<=page.num_pages:
                context['page']=page.page(p)
            else:
                context['page']=page.page(1)
            context['num_pages']=page.num_pages
            for p in context['page']:
                p.setUrl("/cmdb/application/"+str(p.id))
        context['uri']='application'
        context['with_group']=False
        context['with_new']=True
        return render(request, 'list.html',context)
    else:
        if request.method=='POST':
            return 
        else:
            context={}
            re=application.show(appid)
            if re:
                print re
                context['title']="Applications Info"
                context['baseinfo']=re
                return render(request, 'application.html',context)
            else:
                return HttpResponseRedirect("/cmdb/application")

@login_required
def images(request):
    context={}
    context['title']="Image"
    context['uri']='image'
    context['with_group']=False
    context['with_new']=True
    return render(request,'list.html',context)

@login_required
def create_application(request):
    context={}
    context['title']="Create Application"
    context['meth']="new"
    return render(request,'create_application.html',context)

@login_required
def detect_application(request):
    if request.method == 'GET':
        context={}
        context['title']="Detect Application"
        context['meth']="new"
        return render(request,'detect_application.html',context)
    elif request.method == 'POST':
        engine_ip=request.POST['ip']
        host_id=request.POST['hostid']
        engine_port=request.POST['port']
        container_id=request.POST['containerid']
        app_name=request.POST['name']
        app_desc=request.POST['description']
        if engine_ip and host_id and engine_port and container_id and app_name and app_desc:
            application.create_detect(host_id,engine_ip,engine_port,container_id,app_name,app_desc)
            respones={}
            respones['result']='ok'
            return JsonResponse(respones,safe=False)

@login_required
def edit_application(request):
    context={}
    context['title']="Edit Application"
    context['meth']="edit"
    return render(request,'new_edit_application.html',context)

@login_required
def new_image(request):
    context={}
    context['title']="Create Image"
    context['meth']="new"
    return render(request,'new_edit_image.html',context)

@login_required
def edit_image(request):
    context={}
    context['title']="Edit Image"
    context['meth']="edit"
    return render(request,'new_edit_image.html',context)

@login_required
def ping_docker(request):
    if request.method == 'GET':
        ip=request.GET['ip']
        port=request.GET['port']
        if ip and port:
            re=dockerclient.testEngine(ip,port)
            if re:
                respones={}
                respones['result']='ok'
                return JsonResponse(respones,safe=False)
    respones={}
    respones['result']='fail'
    return JsonResponse(respones,safe=False)

@login_required
def list_containers(request):
    if request.method == 'GET':
        ip=request.GET['ip']
        port=request.GET['port']
        if ip and port:
            re=dockerclient.listContainers(ip, port)
            if re:
                return JsonResponse(re,safe=False)
    return JsonResponse([],safe=False)