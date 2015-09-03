from core.models import Host,Resource,PPREPORT,PPMETRICS,PPREPORTLOG,IP
import yaml
import dateutil.parser

def create(cont):
    def construct_ruby_object(loader, suffix, node):
        return loader.construct_yaml_map(node)

    def construct_ruby_sym(loader, node):
        return loader.construct_yaml_str(node)
    
    def timestamp_constructor(loader, node):
        return dateutil.parser.parse(node.value)
    
    yaml.add_multi_constructor(u"!ruby/object:", construct_ruby_object)
    yaml.add_constructor(u"!ruby/sym", construct_ruby_sym)
    yaml.add_constructor(u'tag:yaml.org,2002:timestamp', timestamp_constructor)

    d=yaml.load(cont)
    
    certname=d['host']
    hostname=certname[0:-5]
    
    hosts=Host.objects.filter(name__iexact=hostname)
    if hosts:
        host=hosts.first()
        
        ppreport=PPREPORT()
        ppreport.status=d['status']
        ppreport.time=d['time']
        ppreport.version=d['puppet_version']
        ppreport.save()
        
        for m1 in d['metrics']:
            for m2 in d['metrics'][m1]['values']:
                ppmetrics=PPMETRICS()
                ppmetrics.report=ppreport
                ppmetrics.category=d['metrics'][m1]['name']
                ppmetrics.name=m2[0]
                ppmetrics.value=m2[2]
                ppmetrics.save()
        
        for rel in d['logs']:
            ppreportlog=PPREPORTLOG()
            ppreportlog.report=ppreport
            ppreportlog.level=rel['level']
            ppreportlog.message=rel['message']
            ppreportlog.time=rel['time']
            ppreportlog.save()
        
        res=Resource()
        res.host=host
        res.name=""
        res.type="ppreport"
        res.resource_id=ppreport.id
        res.save()

def showAll():
    rep=PPREPORT.objects.order_by('-time').all()
    return rep

def listByGroup(hostid):
    hosts=Host.objects.filter(id=hostid)
    if hosts:
        re=[]
        host=hosts.first()
        reses=Resource.objects.filter(host=host,type='ppreport').order_by('-id').all()
        for res in reses:
            rep=PPREPORT.objects.filter(id=res.resource_id).first()
            re.append(rep)
        return re

def search(q):
    rep=PPREPORT.objects.all()
    return rep

def show(report_id):
    re={}
    rep=PPREPORT.objects.filter(id=report_id).first()
    re['host']=getHost(rep)
    re['report']=rep
    re['metrics']={}
    re['metrics']['changes']={}
    re['metrics']['events']={}
    re['metrics']['resources']={}
    re['metrics']['time']={}
    met=PPMETRICS.objects.filter(report=rep).all()
    for m in met:
        re['metrics'][str(m.category)][str(m.name)]=m.value
    replog=PPREPORTLOG.objects.filter(report=rep).all()
    re['logs']=replog
    return re
    
def getHost(report):
    res=Resource.objects.filter(resource_id=report.id,type='ppreport')
    if res:
        host=res.first().host
        re=Resource.objects.filter(host=host,type="ip")
        if re:
            ip=IP.objects.filter(id=re.first().resource_id).first()
            return ip.ipv4
