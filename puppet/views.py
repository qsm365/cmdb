from django.http import HttpResponseRedirect,HttpResponse,JsonResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from core import group,host
from puppet import config,parameter,report,enc

# Create your views here.
@login_required
def configs(request,configid=0,groupid=0):
    if (not configid):
        if request.method=='POST':
            meth=request.POST.get('_method','show')
            if meth=='new':
                name=request.POST.get('name')
                description=request.POST.get('description')
                classname=request.POST.get('classname')
                if name and classname:
                    config.create(name, description, classname)
                return HttpResponse("ok")
        else:
            context={}
            q=request.GET.get('q')
            p=int(request.GET.get('page',1))
            if q:
                re=config.search(q)
                context['title']="Configs in search"
            elif groupid:
                re=config.listByGroup(groupid)
                context['title']="Configs in Group"
            else:
                re=config.showAll()
                context['title']="Config List"
            if re:
                page=Paginator(re,10)
                if p>0 and p<=page.num_pages:
                    context['page']=page.page(p)
                else:
                    context['page']=page.page(1)
                context['num_pages']=page.num_pages
                for p in context['page']:
                    p.setUrl("/cmdb/config/"+str(p.id))
            context['grouplist']=group.listByType('CONFIG')
            context['uri']='config'
            context['with_group']=True
            context['with_new']=True
            return render(request,'list.html',context)
    else:
        if request.method=='POST':
            meth=request.POST.get('_method','show')
            if meth=='delete':
                config.delete(configid)
                return HttpResponse("ok")
            if meth=='edit':
                name=request.POST.get('name')
                description=request.POST.get('description')
                classname=request.POST.get('classname')
                if name and classname:
                    config.edit(configid, name, description, classname)
                return HttpResponse("ok")
        else:
            context={}
            context['title']="Config Info"
            context['config']=config.show(configid)
            context['ppfile']=config.ppfile(configid)
            context['host']=config.hostsWithConfig(configid)
            return render(request, 'config.html',context)

@login_required
def parameters(request,function):
    if request.method=="POST":
        if function=='add':
            groupid=request.POST.get("groupid")
            data=eval(request.POST.get("data"))
            if groupid and data:
                for d in data:
                    parameter.createByGroup(groupid,d.keys()[0],d.values()[0])
                return HttpResponse("ok")
        elif function=='remove':
            groupid=request.POST.get("groupid")
            delkey=request.POST.get("key")
            if groupid and delkey:
                parameter.deleteByGroup(groupid,delkey)
                return HttpResponse("ok")
    else:
        if function=='add':
            context={}
            context['title']="Add Group Parameter"
            context['function']=function
            context['hostlist']=group.listByType("Host")
            return render(request,'parameter.html',context)
        elif function=='remove':
            context={}
            context['title']="Remove Group Parameter"
            context['function']=function
            context['hostlist']=group.listByType("Host")
            return render(request,'parameter.html',context)

@login_required
def reports(request,report_id=0,groupid=0):
    if report_id:
        context=report.show(report_id)
        context['title']="Report Detail"
        return render(request,'report.html',context)
    else:
        context={}
        p=int(request.GET.get('page',1))
        if groupid:
            re=report.listByHost(groupid)
            context['title']="Reports in Group"
        else:
            re=report.showAll()
            context['title']="Report List"
        if re:
            page=Paginator(re,10)
            if p>0 and p<=page.num_pages:
                context['page']=page.page(p)
            else:
                context['page']=page.page(1)
            context['num_pages']=page.num_pages
            for p in context['page']:
                p.setHost(report.getHost(p))
                p.setUrl("/cmdb/report/"+str(p.id))
        context['grouplist']=host.showAll()
        context['uri']="report"
        context['with_new']=False
        context['with_group']=True
        context['nosearch']=True
        return render(request,'list.html',context)

def externalNodeClassifier(request):
    return HttpResponse(enc.get(request.GET['certname']),content_type='text/yaml')

@csrf_exempt
def importReport(request):
    cont=request.body
    if cont:
        report.create(cont)
        return HttpResponse("ok")
    else:
        return HttpResponseNotFound("404")

@login_required
def new_config(request):
    context={}
    context['title']="Create Config"
    context['meth']="new"
    return render(request,'new_edit_config.html',context)

@login_required
def edit_config(request,configid=0):
    re=config.show(configid)
    if re:
        context={}
        context['title']="Config Edit"
        context['config']=re
        context['meth']="edit"
        return render(request, 'new_edit_config.html',context)
    else:
        return HttpResponseRedirect("/cmdb/config")

@login_required
def config_find_json(request):
    if request.method=='GET':
        if len(request.GET['q'])>=3:
            re=config.search(request.GET['q'])
            if re:
                respones=[]
                for i in re:
                    s={}
                    s['id']=i.id
                    s['name']=i.name
                    s['classname']=i.classname
                    respones.append(s)
                return JsonResponse(respones,safe=False)
    return JsonResponse([],safe=False)

@login_required
def parameter_find_json(request):
    if request.method == 'GET':
        gid=request.GET['groupid']
        if gid:
            re=parameter.listByGroup(gid)
            if re:
                respones=[]
                for i in re:
                    s={}
                    s['id']=i.id
                    s['key']=i.key
                    s['value']=i.value
                    respones.append(s)
                return JsonResponse(respones,safe=False)
    return JsonResponse([],safe=False)