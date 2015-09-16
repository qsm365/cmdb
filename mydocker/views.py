from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mydocker import dockerclient,application,image
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
            meth=request.POST.get('_method','show')
            if meth=='delete':
                application.delete(appid)
                return HttpResponse("ok")
            if meth=='edit':
                name=request.POST.get('name')
                description=request.POST.get('description')
                if name:
                    application.edit(appid, name, description)
                return HttpResponse("ok")
        else:
            context={}
            re=application.show(appid)
            if re:
                inspect=dockerclient.inspect_container(re.engineip,re.engineport,re.containername)
                context['title']="Applications Info"
                context['baseinfo']=re
                context['inspect']=inspect
                return render(request, 'application.html',context)
            else:
                return HttpResponseRedirect("/cmdb/application")

@login_required
def images(request,imgid=0):
    if not imgid:
        context={}
        q=request.GET.get('q')
        p=int(request.GET.get('page',1))
        if q:
            re=image.search(q)
            context['title']="Image in search"
        else:
            re=image.showAll()
            context['title']="Image List"
        if re:
            page=Paginator(re,10)
            if p>0 and p<=page.num_pages:
                context['page']=page.page(p)
            else:
                context['page']=page.page(1)
            context['num_pages']=page.num_pages
            for p in context['page']:
                p.setUrl("/cmdb/image/"+str(p.id))
        context['uri']='image'
        context['with_group']=False
        context['with_new']=True
        return render(request,'list.html',context)
    else:
        if request.method=='POST':
            meth=request.POST.get('_method','show')
            if meth=='delete':
                image.delete(imgid)
                return HttpResponse("ok")
        else:
            context={}
            re=image.show(imgid)
            if re:
                context['title']="Image Info"
                context['baseinfo']=re
                context['apps']=image.getAppByImage(re.id)
                return render(request, 'image.html',context)

@login_required
def new_application(request):
    context={}
    context['title']="New Application"
    return render(request,'new_application.html',context)

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
def edit_application(request,appid=0):
    re=application.show(appid)
    if re:
        context={}
        context['title']="Edit Application"
        context['baseinfo']=re
        context['meth']="edit"
        return render(request,'edit_application.html',context)
    else:
        return HttpResponseRedirect("/cmdb/application")
        

@login_required
def new_image(request):
    if request.method == 'GET':
        context={}
        context['title']="Create Image"
        context['meth']="new"
        return render(request,'new_image.html',context)
    elif request.method == 'POST':
        registry_ip=request.POST['ip']
        registry_port=request.POST['port']
        repository=request.POST['repository']
        tag=request.POST['tag']
        image_id=request.POST['image_id']
        if registry_ip and registry_port and repository and tag and image_id:
            image.create(registry_ip, registry_port, repository, tag, image_id)
            respones={}
            respones['result']='ok'
            return JsonResponse(respones,safe=False)

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

@login_required
def ping_registry(request):
    if request.method == 'GET':
        ip=request.GET['ip']
        port=request.GET['port']
        if ip and port:
            re=dockerclient.testRegistry(ip, port)
            if re:
                respones={}
                respones['result']='ok'
                return JsonResponse(respones,safe=False)
    respones={}
    respones['result']='fail'
    return JsonResponse(respones,safe=False)

@login_required
def list_images(request):
    if request.method == 'GET':
        ip=request.GET['ip']
        port=request.GET['port']
        if ip and port:
            re=dockerclient.showAllRegistryTag(ip, port)
            if re:
                return JsonResponse(re,safe=False)
    return JsonResponse([],safe=False)