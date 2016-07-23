import requests
import json

headers = {'content-type':'application/json'}

def createImage(uri,name,container_format,disk_format,tokenid):
    url=uri+"/v2/images"
    headers['X-Auth-Token']=tokenid
    data={}
    data['name']=name
    data['container_format']=container_format
    data['disk_format']=disk_format
    result=requests.post(url,data=json.dumps(data),headers=headers,timeout=5)
    if result.status_code in [200,201]:
        re=result.json()
        return re
    else:
        return result.status_code

#def uploadImage(uri,imageid,path,tokenid):
#    url=uri+"/v2/images/"+str(imageid)
#    headers['X-Auth-Token']=tokenid
#    headers['content-type']='application/octet-stream'
#    result=requests.put(url,headers=headers)
#    if result.status_code in [200,204]:
#        return "ok"
#    else:
#        return result.status_code
    
def listImages(uri,tokenid):
    url=uri+"/v2/images"
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers,timeout=5)
    if result.status_code in [200]:
        re = result.json()
        r=[]
        for s in re['images']:
            r.append(s)
        return r
    else:
        return result.status_code

def ImageDetail(uri,imageid,tokenid):
    url=uri+"/v2/images/"+str(imageid)
    headers['X-Auth-Token']=tokenid
    result=requests.get(url,headers=headers,timeout=5)
    if result.status_code in [200]:
        re = result.json()
        return re
    else:
        return result.status_code
    
def deleteImage(uri,imageid,tokenid):
    url=uri+"/v2/images/"+str(imageid)
    headers['X-Auth-Token']=tokenid
    result=requests.delete(url,headers=headers,timeout=5)
    if result.status_code in [200,202]:
        return "ok"
    else:
        return result.status_code