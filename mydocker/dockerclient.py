from docker.utils import create_host_config
from docker import Client
from _mysql import result
import requests

def testEngine(engine_ip,engine_port):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
        result=cli.ping()
        if result=="OK":
            return True
    except Exception:
        return False
    return False

def listContainers(engine_ip,engine_port):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
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

def updateContainerStatus(engine_ip,engine_port,container_id):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
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

def create(engine_ip,engine_port,imagename,command,entrypoint,container_name,host_name,network_mode,privileged,security_opt,ulimit_nofile,ulimit_noproc,ports,port_bindings,volume,binds,dns_server,hosts,environment):
    #try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
        
        host_config=create_host_config(binds=binds,
                                        port_bindings=port_bindings,
                                        privileged=privileged,
                                        network_mode=network_mode,
                                        security_opt=security_opt,
                                        extra_hosts=hosts)
        
        container = cli.create_container(image=imagename, \
                                         command=command, \
                                         entrypoint=entrypoint, \
                                         hostname=host_name, \
                                         detach=True, \
                                         name=container_name, \
                                         ports=ports, \
                                         volumes=volume ,\
                                         environment=environment, \
                                         host_config=host_config )
        
        result=cli.inspect_container(container['Id'])
        ret={}
        ret['container_id']=result['Id']
        ret['container_name']=result['Name']
        ret['image']=result['Image']
        ret['created']=result['Created']
        ret['msg']=container['Warnings']
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
            ret['status']="stopped"
        return ret
    #except Exception,ex:
    #    return str(Exception,":",ex)

def detect(engine_ip,engine_port,container_id):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
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
            ret['status']="stopped"
        return ret
    except Exception:
        return

def inspect_container(engine_ip,engine_port,container_id):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
        result=cli.inspect_container(container_id)
        
        return result
    except Exception:
        return

def pull(engine_ip,engine_port,imagename):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
        result=cli.pull(imagename, stream=False,insecure_registry=True)
        return result
    except Exception:
        return

def start(engine_ip,engine_port,container_id):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
        cli.start(container_id)
    except Exception:
        return

def stop(engine_ip,engine_port,container_id):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
        cli.stop(container_id,15)
    except Exception:
        return

def kill(engine_ip,engine_port,container_id):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
        cli.kill(container_id)
    except Exception:
        return

def remove_container(engine_ip,engine_port,container_id):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
        cli.remove_container(container_id, False, False, False)
    except Exception:
        return
    
def remove_image(engine_ip,engine_port,image_id):
    try:
        cli=Client(base_url="tcp://"+engine_ip+":"+engine_port)
        cli.remove_image(image_id, False, True)
    except Exception:
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
