from django.http import HttpResponseRedirect,HttpResponse,JsonResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageDraw, ImageFont
import cStringIO, string, os, random
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import render
from django.core.paginator import Paginator
from urllib import unquote

from core import host,config,group,parameter,enc,report
# Create your views here.

@csrf_exempt
def collector(request):
    if request.method=='POST':
        content=host.resolve(request.body)
        ip=host.get_client_ip(request)
        hostid=host.exists(content['hostname'], ip)
        if hostid:
            host.update(hostid, content, ip)
        else:
            host.create(content,ip)
        return HttpResponse("ok")
    else:
        return HttpResponseRedirect("/cmdb/login")

@login_required
def hosts(request,hostid=0,groupid=0):
    if not hostid:
        context={}
        q=request.GET.get('q')
        p=int(request.GET.get('page',1))
        if q:
            re=host.search(q)
            context['title']="Hosts in search"
        elif groupid:
            re=host.listByGroup(groupid)
            context['title']="Hosts in Group"
        else:
            re=host.showAll()
            context['title']="Host List"
        if re:
            page=Paginator(re,10)
            if p>0 and p<=page.num_pages:
                context['page']=page.page(p)
            else:
                context['page']=page.page(1)
            context['num_pages']=page.num_pages
            for p in context['page']:
                p.setIP(host.getIP(p.id))
                p.setUrl("/cmdb/host/"+str(p.id))
        context['grouplist']=group.listByType('Host')
        context['uri']='host'
        context['with_group']=True
        context['with_new']=True
        return render(request, 'list.html',context)
    else:
        if request.method=='POST':
            meth=request.POST.get('_method','show')
            if meth=='delete':
                host.delete(hostid)
                return HttpResponse("ok")
            elif meth=='edit_desc':
                desc=unquote(request.POST.get('desc',''))
                host.edit_desc(hostid,desc)
                return HttpResponse("ok")
            elif meth=='addparam':
                key=request.POST.get('key')
                value=request.POST.get('value')
                return HttpResponse(parameter.createByHost(hostid,key,value))
            elif meth=='delparam':
                pid=request.POST.get('pid')
                parameter.delete(pid)
                return HttpResponse("ok")
        else:
            re=host.show(hostid)
            if re:
                context=re
                context['title']="Host Info"
                return render(request, 'host.html',context)
            else:
                return HttpResponseRedirect("/cmdb/host")

@login_required
def groups(request,groupid=0,grouptype=""):
    if (not groupid):
        if request.method=='POST':
            meth=request.POST.get('_method','show')
            if meth=='new':
                name=request.POST.get('name')
                t=request.POST.get('type')
                member=request.POST.get('member')
                if name and t and member:
                    m=member.split(';')
                    m.pop(-1)
                    group.addMember(group.create(name, t), m)
                return HttpResponse("ok")
        else:
            context={}
            q=request.GET.get('q')
            p=int(request.GET.get('page',1))
            if q:
                re=group.search(q)
                context['title']="Groups in search"
            elif grouptype:
                re=group.listByType(grouptype)
                context['title']=grouptype.capitalize()+" Groups Manage"
            else:
                re=group.showAll()
                context['title']="Group List"
            if re:
                page=Paginator(re,10)
                if p>0 and p<=page.num_pages:
                    context['page']=page.page(p)
                else:
                    context['page']=page.page(1)
                context['num_pages']=page.num_pages
                for p in context['page']:
                    p.setUrl("/cmdb/group/"+str(p.id))
            context['uri']='group'
            context['with_group']=False
            context['with_new']=True
            return render(request,'list.html',context)
    else:
        if request.method=="POST":
            meth=request.POST.get('_method','show')
            if meth=='delete':
                group.delete(groupid)
                return HttpResponse("ok")
            if meth=='edit':
                name=request.POST.get('name')
                add_list=request.POST.get('add')
                if add_list:
                    group.addMember(groupid, add_list.split(','))
                del_list=request.POST.get('del')
                if del_list:
                    group.delMember(groupid, del_list.split(','))
                group.changeName(groupid, name)
                return HttpResponse("ok")
        else:
            re=group.show(groupid)
            if re:
                context={}
                context['group']=group.show(groupid)
                context['members']=group.getMember(groupid)
                context['title']="Group Info"
                if context['group'].type=="Host":
                    for p in context['members']:
                        p.setIP(host.getIP(p.id))
                return render(request,'group.html',context)
            else:
                return HttpResponseRedirect("/cmdb/group")

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
def manage(request):
    context={}
    context['title']="Manage"
    return render(request,'manage.html',context)

@login_required
def relationship(request,function,functype=''):
    if request.method=="POST":
        if function=='add':
            if functype=='single2single':
                hosts=request.POST.get('host')
                configs=request.POST.get('config')
                if hosts and config:
                    h=host.get(hosts)
                    c=config.get(configs)
                    if h and c:
                        host.addConfig(h, c)
            elif functype=='group2single':
                hosts=request.POST.get('host')
                configs=request.POST.get('config')
                if hosts and config:
                    h=host.get(hosts)
                    configlist=group.getMember(configs)
                    if h and configlist:
                        for c in configlist:
                            host.addConfig(h, c)
            elif functype=='single2group':
                hosts=request.POST.get('host')
                configs=request.POST.get('config')
                if hosts and config:
                    hostlist=group.getMember(hosts)
                    c=config.get(configs)
                    if hostlist and c:
                        for h in hostlist:
                            host.addConfig(h, c)
            elif functype=='group2group':
                hosts=request.POST.get('host')
                configs=request.POST.get('config')
                if hosts and config:
                    hostlist=group.getMember(hosts)
                    configlist=group.getMember(configs)
                    if hostlist and configlist:
                        for h in hostlist:
                            for c in configlist:
                                host.addConfig(h, c)
        if function=='remove':
            hosts=request.POST.get('host')
            configs=request.POST.get('config')
            if functype=='single2single':
                hosts=request.POST.get('host')
                configs=request.POST.get('config')
                if hosts and config:
                    h=host.get(hosts)
                    c=config.get(configs)
                    if h and c:
                        host.removeConfig(h, c)
            elif functype=='group2single':
                hosts=request.POST.get('host')
                configs=request.POST.get('config')
                if hosts and config:
                    h=host.get(hosts)
                    configlist=group.getMember(configs)
                    if h and configlist:
                        for c in configlist:
                            host.removeConfig(h, c)
            elif functype=='single2group':
                hosts=request.POST.get('host')
                configs=request.POST.get('config')
                if hosts and config:
                    hostlist=group.getMember(hosts)
                    c=config.get(configs)
                    if hostlist and c:
                        for h in hostlist:
                            host.removeConfig(h, c)
            elif functype=='group2group':
                hosts=request.POST.get('host')
                configs=request.POST.get('config')
                if hosts and config:
                    hostlist=group.getMember(hosts)
                    configlist=group.getMember(configs)
                    if hostlist and configlist:
                        for h in hostlist:
                            for c in configlist:
                                host.removeConfig(h, c)
        return HttpResponse("ok")
    else:
        context={}
        context['title']="Host and Config Relationship Manage"
        context['function']=function
        context['hostlist']=host.showAll()
        context['configlist']=config.showAll()
        context['hostgrouplist']=group.listByType("Host")
        context['configgrouplist']=group.listByType("CONFIG")
        return render(request,'relationship.html',context)

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
            re=report.listByGroup(groupid)
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
def home(request):
    context={}
    context['title']="Home"
    return render(request,'home.html',context)

@login_required
def new_group(request):
    context={}
    context['title']="Create Group"
    context['type']=["Host","CONFIG"]
    context['meth']='new'
    return render(request,'new_group.html',context)

@login_required
def new_config(request):
    context={}
    context['title']="Create Config"
    context['meth']="new"
    return render(request,'new_edit_config.html',context)

@login_required
def edit_group(request,groupid=0):
    re=group.show(groupid)
    if re:
        context={}
        context['title']="Group Edit"
        context['group']=re
        context['members']=group.getMember(groupid)
        if context['group'].type=="Host":
            for p in context['members']:
                p.setIP(host.getIP(p.id))
        return render(request, 'edit_group.html',context)
    else:
        return HttpResponseRedirect("/cmdb/group")

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
def host_find_json(request):
    if request.method == 'GET':
        if len(request.GET['q'])>=3:
            re=host.search(request.GET['q'])
            if re:
                respones=[]
                for i in re:
                    s={}
                    s['id']=i.id
                    s['name']=i.name
                    s['ip']=host.getIP(i.id)
                    respones.append(s)
                return JsonResponse(respones,safe=False)
    return JsonResponse([],safe=False)

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

def login(request):
    if request.method == 'GET':
        return render_to_response('login.html', RequestContext(request))
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        imagecode= request.POST.get('imagecode','')
        if imagecode.lower()!=request.session['captcha']:
            return render_to_response('login.html', RequestContext(request, {'imagecode_is_wrong':True}))
        
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/cmdb")
        else:
            return render_to_response('login.html', RequestContext(request, {'password_is_wrong':True}))
    

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/cmdb/login")

def captcha(request):
    '''Captcha'''
    image = Image.new('RGB', (128, 49), color = (255, 255, 255))
    # model, size, background color
    font_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'arial.ttf')
    # choose a font file
    font = ImageFont.truetype(font_file, 39)
    # the font object
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.letters + string.digits, 4))
    # The random string
    j=0
    for i in rand_str:
        draw.text((7+28*j, 1), i, fill=(random.randint(0,200), random.randint(0,200), random.randint(0,200)), font=font)
        j=j+1
    # position, content, color, font
    del draw
    request.session['captcha'] = rand_str.lower()
    # store the content in Django's session store
    buf = cStringIO.StringIO()
    # a memory buffer used to store the generated image
    image.save(buf, 'jpeg')
    return HttpResponse(buf.getvalue(), 'image/jpeg')
    # return the image data stream as image/jpeg format, browser will treat it as an image
