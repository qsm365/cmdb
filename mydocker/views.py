from django.http import JsonResponse,HttpResponseRedirect,HttpResponse,HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mydocker import dockerclient,application,image
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from json import JSONDecoder

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
            for pa in context['page']:
                pa.setUrl("/cmdb/application/"+str(pa.id))
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
            if meth=='start':
                app=application.show(appid)
                containerid=app.containerid
                ip=app.engineip
                port=app.engineport
                dockerclient.start(ip, port, containerid)
                application.updateStatus(app)
                return HttpResponse("ok")
            if meth=='stop':
                app=application.show(appid)
                containerid=app.containerid
                ip=app.engineip
                port=app.engineport
                dockerclient.stop(ip, port, containerid)
                application.updateStatus(app)
                return HttpResponse("ok")
        else:
            context={}
            re=application.show(appid)
            if re:
                inspect=dockerclient.inspect_container(re.engineip,re.engineport,re.containername)
                context['title']="Applications Info"
                context['baseinfo']=re
                context['inspect']=inspect
                return render(request, 'docker/application.html',context)
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
            for pa in context['page']:
                pa.setUrl("/cmdb/image/"+str(pa.id))
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
                return render(request, 'docker/image.html',context)

@login_required
def new_application(request):
    context={}
    context['title']="New Application"
    return render(request,'docker/new_application.html',context)

@login_required
def create_application(request):
    if request.method == 'GET':
        context={}
        context['title']="Create Application"
        context['images']=image.showAll()
        return render(request,'docker/create_application.html',context)
    elif request.method == 'POST':
        meth=request.POST['meth']
        ip=request.POST['ip']
        port=request.POST['port']
        imagename=request.POST['imagename']
        if meth=='pull':
            re=dockerclient.pull(ip, port, imagename)
            if re:
                respones={}
                respones['result']='ok'
                respones['msg']=re
                return JsonResponse(respones,safe=False)
            else:
                respones={}
                respones['result']='fail'
                return JsonResponse(respones,safe=False)
        elif meth=="create":
            hostid=request.POST['hostid']
            name=request.POST['name']
            description=request.POST['description']
            
            l_command=request.POST['command']
            l_entrypoint=request.POST['entrypoint']
            container_name=request.POST['container_name']
            host_name=request.POST['host_name']
            network_mode=request.POST['network_mode']
            privileged=True if request.POST['privileged']=="true" else False
            l_security_opt=request.POST['security_opt']
            ulimit_nofile=request.POST['ulimit_nofile']
            ulimit_noproc=request.POST['ulimit_noproc']
            arr_ports = JSONDecoder().decode(request.POST['ports'])
            arr_volum = JSONDecoder().decode(request.POST['volum'])
            arr_dns_server = JSONDecoder().decode(request.POST['dns_server'])
            arr_hosts = JSONDecoder().decode(request.POST['hosts'])
            arr_environment = JSONDecoder().decode(request.POST['environment'])
            ports=[]
            port_bindings={}
            command=[]
            command=l_command.split(";")
            entrypoint=[]
            entrypoint=l_entrypoint.split(";")
            security_opt=[]
            security_opt=l_security_opt.split(";")
            for p in arr_ports:
                if p.split(":")[0]:
                    port_bindings[int(p.split(":")[0])]=int(p.split(":")[1])
                    ports.append(int(p.split(":")[0]))
            print port_bindings
            print ports
            volume=[]
            binds={}
            for v in arr_volum:
                vv={}
                if v.split(":")[0]:
                    vv['bind']=v.split(":")[1]
                    vv['mode']='rw'
                    volume.append(v.split(":")[1])
                    binds[v.split(":")[0]]=vv
            dns_server=[]
            for d in arr_dns_server:
                if d:
                    dns_server.append(d)
            hosts={}
            for h in arr_hosts:
                if h.split(":")[0]:
                    hosts[h.split(":")[0]]=h.split(":")[1]
            environment={}
            for e in arr_environment:
                if e.split(":")[0]:
                    environment[e.split(":")[0]]=e.split(":")[1]
            msg=application.create_new(ip, 
                                       port, 
                                       hostid, 
                                       name, 
                                       description, 
                                       imagename,
                                       command,
                                       entrypoint, 
                                       container_name, 
                                       host_name, 
                                       network_mode, 
                                       privileged, 
                                       security_opt, 
                                       ulimit_nofile, 
                                       ulimit_noproc, 
                                       ports, 
                                       port_bindings, 
                                       volume, 
                                       binds, 
                                       dns_server, 
                                       hosts,
                                       environment)
            respones={}
            respones['result']='ok'
            respones['msg']=msg
            return JsonResponse(respones,safe=False)

@login_required
def detect_application(request):
    if request.method == 'GET':
        context={}
        context['title']="Detect Application"
        context['meth']="new"
        return render(request,'docker/detect_application.html',context)
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
        return render(request,'docker/edit_application.html',context)
    else:
        return HttpResponseRedirect("/cmdb/application")
        
@login_required
def new_image(request):
    if request.method == 'GET':
        context={}
        context['title']="Create Image"
        context['meth']="new"
        return render(request,'docker/new_image.html',context)
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

@csrf_exempt
def container_update(request):
    if request.method == 'GET':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        port="2375"
        if ip and port:
            ping=dockerclient.testEngine(ip, port)
            if ping:
                re1=dockerclient.listContainers(ip,port)
                re2=application.listByIp(ip)
                if re1:
                    for re in re1:
                        #auto detect
                        if not application.exist(re['id']):
                            application.auto_detect(ip, port, re['id'])
                if re2:    
                    for re in re2:
                        #update status
                        application.updateStatus(re)
                return HttpResponse("ok")
    return HttpResponseNotFound("403")