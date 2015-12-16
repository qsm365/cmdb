import requests
import json
import datetime

headers = {'content-type':'application/json'}

def listServers(uri,tokenid):
    url=uri+"/servers/detail"
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200,203]:
        re = result.json()
        r=[]
        for s in re['servers']:
            r.append(s)
        return r
    else:
        return result.status_code
        
def serverDetail(uri,serverid,tokenid):
    url=uri+"/servers/"+str(serverid)
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200,203]:
        re = result.json()
        return re['server']
    else:
        return result.status_code
        
#def createServer(url,tokenid):
 
#def deleteServer(uri,sid,tokenid):
            
def listFlavors(uri,tokenid):
    url=uri+"/flavors"
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200]:
        re = result.json()
        r={}
        for f in re['flavors']:
            r[f['id']]=f['name']
        return r
    else:
        return result.status_code
        
def flavorDetail(uri,flavorid,tokenid):
    url=uri+"/flavors/"+str(flavorid)
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200]:
        re = result.json()
        r={}
        r['vcpus']=re['flavor']['vcpus']
        r['ram']=re['flavor']['ram']
        r['swap']=re['flavor']['swap'] if re['flavor']['swap'] else 0
        r['disk']=re['flavor']['disk']
        return r
    else:
        return result.status_code
    
def createFlavor(uri,name,vcpus,ram,swap,disk,tokenid):
    url=uri+"/flavors"
    headers['X-Auth-Token']=tokenid
    data={}
    flavor={}
    flavor['name']=name
    flavor['vcpus']=vcpus
    flavor['ram']=ram
    flavor['swap']=swap
    flavor['disk']=disk
    data['flavor']=flavor
    result=requests.post(url,data=json.dumps(data),headers=headers)
    if result.status_code in [200]:
        re=result.json()
        return re['flavor']['id']
    else:
        return result.status_code
             
def deleteFlavor(uri,flavorid,tokenid):
    url=uri+"/flavors/"+str(flavorid)
    headers['X-Auth-Token']=tokenid
    result=requests.delete(url,headers=headers)
    if result.status_code in [200]:
        return "ok"
    else:
        return result.status_code
    
def listKeypairs(uri,tokenid):
    url=uri+"/os-keypairs"
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200]:
        re = result.json()
        r=[]
        for k in re['keypairs']:
            del k['keypair']['public_key']
            r.append(k['keypair'])
        return r
    else:
        return result.status_code
    
def keypairDetail(uri,name,tokenid):
    url=uri+"/os-keypairs/"+str(name)
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200]:
        re = result.json()
        r={}
        r['public_key'] = re['keypair']['public_key']
        r['name'] = re['keypair']['name']
        r['fingerprint'] = re['keypair']['fingerprint']
        r['created_at'] = datetime.datetime.strptime(re['keypair']['created_at'],'%Y-%m-%dT%H:%M:%S.%f')
        return r
    else:
        return result.status_code
    
def deleteKeypair(uri,name,tokenid):
    url=uri+"/os-keypairs/"+str(name)
    headers['X-Auth-Token']=tokenid
    result=requests.delete(url,headers=headers)
    if result.status_code in [200]:
        return "ok"
    else:
        return result.status_code
    
def createKeypair(uri,name,tokenid):
    url=uri+"/os-keypairs"
    headers['X-Auth-Token']=tokenid
    data={}
    keypair={}
    keypair['name']=name
    data['keypair']=keypair
    result=requests.post(url,data=json.dumps(data),headers=headers)
    if result.status_code in [200,201]:
        re = result.json()
        r={}
        r['public_key'] = re['keypair']['public_key']
        r['private_key'] = re['keypair']['private_key']
        r['name'] = re['keypair']['name']
        r['fingerprint'] = re['keypair']['fingerprint']
        return r
    else:
        return result.status_code
    
def importKeypair(uri,name,public_key,tokenid):
    url=uri+"/os-keypairs"
    headers['X-Auth-Token']=tokenid
    data={}
    keypair={}
    keypair['name']=name
    keypair['public_key']=public_key
    data['keypair']=keypair
    result=requests.post(url,data=json.dumps(data),headers=headers)
    if result.status_code in [200,201]:
        re = result.json()
        r={}
        r['public_key'] = re['keypair']['public_key']
        r['name'] = re['keypair']['name']
        r['fingerprint'] = re['keypair']['fingerprint']
        return r
    else:
        return result.status_code

def reserveIp(uri,ipaddress,tokenid):
    url=uri+"/os-fixed-ips/"+str(ipaddress)+"/action"
    headers['X-Auth-Token']=tokenid
    data={}
    data['reserve']=None
    result=requests.post(url,data=json.dumps(data),headers=headers)
    if result.status_code in [200,202]:
        return "ok"
    else:
        return result.status_code

def unreserveIp(uri,ipaddress,tokenid):
    url=uri+"/os-fixed-ips/"+str(ipaddress)+"/action"
    headers['X-Auth-Token']=tokenid
    data={}
    data['unreserve']=None
    result=requests.post(url,data=json.dumps(data),headers=headers)
    if result.status_code in [200,202]:
        return "ok"
    else:
        return result.status_code

def listNetwork(uri,tokenid):
    url=uri+"/os-networks"
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200]:
        re = result.json()
        r=[]
        for n in re['networks']:
            nn={}
            nn['label']=n['label']
            nn['id']=n['id']
            nn['created_at']=datetime.datetime.strptime(n['created_at'],'%Y-%m-%dT%H:%M:%S.%f')
            nn['bridge']=n['bridge']
            nn['gateway']=n['gateway']
            nn['netmask']=n['netmask']
            nn['cidr']=n['cidr']
            nn['dhcp_server']=n['dhcp_server']
            nn['dhcp_start']=n['dhcp_start']
            nn['dns1']=n['dns1']
            nn['dns2']=n['dns2']
            r.append(nn)
        return r
    else:
        return result.status_code

def networkDetail(uri,nid,tokenid):
    url=uri+"/os-networks/"+str(nid)
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200]:
        re = result.json()
        n = re['network']
        r={}
        r['label']=n['label']
        r['id']=n['id']
        r['created_at']=datetime.datetime.strptime(n['created_at'],'%Y-%m-%dT%H:%M:%S.%f')
        r['bridge']=n['bridge']
        r['gateway']=n['gateway']
        r['netmask']=n['netmask']
        r['cidr']=n['cidr']
        r['dhcp_server']=n['dhcp_server']
        r['dhcp_start']=n['dhcp_start']
        r['dns1']=n['dns1']
        r['dns2']=n['dns2']
        return r
    else:
        return result.status_code

def deleteNetwork(uri,nid,tokenid):
    url=uri+"/os-networks/"+str(nid)
    headers['X-Auth-Token']=tokenid
    result=requests.delete(url,headers=headers)
    if result.status_code in [200,202]:
        return "ok"
    else:
        return result.status_code

def createNetwork(uri,label,cidr,tokenid,**args):
    url=uri+"/os-networks"
    headers['X-Auth-Token']=tokenid
    data={}
    network=args
    network['label']=label
    network['cidr']=cidr
    data['network']=network
    result=requests.post(url,data=json.dumps(data),headers=headers)
    if result.status_code in [200,202]:
        re=result.json()
        return re
    else:
        return result.status_code
