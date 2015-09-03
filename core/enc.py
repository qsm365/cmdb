import yaml
from models import Host,Resource,CONFIG,PARAMETER


def get(cert_name):
    hostname=cert_name[0:-5]
    hosts=Host.objects.filter(name__iexact=hostname)
    if hosts:
        host=hosts.first()
        res1=Resource.objects.filter(host=host,type='config').all()
        classes=[]
        if res1:
            for r in res1:
                cs=CONFIG.objects.filter(id=r.resource_id)
                if cs:
                    c=cs.first()
                    classes.append(str(c.classname))
                    
        res2=Resource.objects.filter(host=host,type='parameter').all()
        parameters={}
        if res2:
            for r in res2:
                ps=PARAMETER.objects.filter(id=r.resource_id)
                if ps:
                    p=ps.first()
                    parameters[str(p.key)]=str(p.value)
                    
        result={}
        result['name']=str(cert_name)
        if classes:
            result['classes']=classes
        if parameters:
            result['parameters']=parameters
        return yaml.safe_dump(result,default_flow_style=False,explicit_start=True)
    else:
        return "---\nclasses: []\n"
