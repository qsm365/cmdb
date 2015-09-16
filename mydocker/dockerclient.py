from docker import Client
from _mysql import result
import requests

def testEngine(engine_ip,engine_port):
    cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
    try:
        result=cli.ping()
        if result=="OK":
            return True
    except Exception:
        return False
    return False

def listContainers(engine_ip,engine_port):
    cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
    try:
        result=cli.containers(all=True)
        ret=[]
        for re in result:
            r={}
            r['id']=re['Id']
            r['name']=re['Names'][0]
            r['image']=re['Image']
            ret.append(r)
        return ret
    except Exception:
        return

def getStatus(engine_ip,engine_port,container_id):
    cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
    try:
        result=cli.inspect_container(container_id)
        state=result['State']
        if state['Running']:
            return "running"
        elif state['Restarting']:
            return "restarting"
        elif state['Paused']:
            return "paused"
        elif state['Dead']:
            return "dead"
        else:
            return "stopped"
    except Exception:
        return "error"

def create():
    return

def detect(engine_ip,engine_port,container_id):
    cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
    try:
        result=cli.inspect_container(container_id)
        ret={}
        ret['container_id']=result['Id']
        ret['container_name']=result['Name']
        ret['image']=result['Image']
        ret['created']=result['Created']
        state=result['State']
        ret['status']="unkonown"
        if state['Running']:
            ret['status']="running"
        elif state['Restarting']:
            ret['status']="restarting"
        elif state['Paused']:
            ret['status']="pause"
        elif state['Dead']:
            ret['status']="dead"
        else:
            ret['status']="stop"
        return ret
    except Exception:
        return

def inspect_container(engine_ip,engine_port,container_id):
    cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
    try:
        result=cli.inspect_container(container_id)
        
        return result
    except Exception:
        return

def start():
    return

def stop():
    return

def kill():
    return

def remove():
    return

def testRegistry(registry_ip,registry_port):
    try:
        r=requests.get('http://'+registry_ip+":"+registry_port+"/v1/_ping")
        if r.status_code==200:
            return True
        else:
            return False
    except Exception:
        return False
    
def showAllRegistryTag(registry_ip,registry_port):
    try:
        r=requests.get('http://'+registry_ip+":"+registry_port+"/v1/search?q=")
        if r.status_code==200:
            result=[]
            re=r.json()
            repos=re['results']
            for repo in repos:
                r=requests.get('http://'+registry_ip+":"+registry_port+"/v1/repositories/"+repo['name']+"/tags")
                re=r.json()
                for k,v in re.items():
                    t={}
                    t['name']=repo['name']
                    t['tag']=k
                    t['image_id']=v
                    result.append(t)
            return result
    except Exception:
        return

def showRegistryImage(registry_ip,registry_port,image_id):
    try:
        r=requests.get('http://'+registry_ip+":"+registry_port+"/v1/images/"+image_id+"/json")
        if r.status_code==200:
            re=r.json()
            return re
    except Exception:
        return