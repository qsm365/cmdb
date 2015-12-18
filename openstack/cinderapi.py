import requests
import json

headers = {'content-type':'application/json'}

def createVolume(uri,name,size,tokenid,**args):
    url=uri+"/volumes"
    headers['X-Auth-Token']=tokenid
    data={}
    volume=args
    volume['name']=name
    volume['size']=size
    data['volume']=volume
    result=requests.post(url,data=json.dumps(data),headers=headers)
    if result.status_code in [200,202]:
        re=result.json()
        return re
    else:
        return result.status_code
    
def listVolumes(uri,tokenid):
    url=uri+"/volumes/detail"
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200]:
        re = result.json()
        r=[]
        for s in re['volumes']:
            r.append(s)
        return r
    else:
        return result.status_code

def volumeDetail(uri,volumeid,tokenid):
    url=uri+"/volumes/"+str(volumeid)
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers)
    if result.status_code in [200]:
        re = result.json()
        return re['volume']
    else:
        return result.status_code
    
def deleteVolume(uri,volumeid,tokenid):
    url=uri+"/volumes/"+str(volumeid)
    headers['X-Auth-Token']=tokenid
    result=requests.delete(url,headers=headers)
    if result.status_code in [200,202]:
        return "ok"
    else:
        return result.status_code