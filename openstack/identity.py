import requests
import json
import datetime

headers = {'content-type':'application/json'}

def authenticate(ksIP,ksPort,tenant,user,passwd):
    url='http://'+ksIP+':'+str(ksPort)+'/v2.0/tokens'
    data={}
    auth={}
    auth['tenantName']=tenant
    passwordCredentials={}
    passwordCredentials['username']=user
    passwordCredentials['password']=passwd
    auth['passwordCredentials']=passwordCredentials
    data['auth']=auth
    result=requests.post(url,data=json.dumps(data),headers=headers)
    if result.status_code in [200,203]:
        re=result.json()
        r={}
        r['tokenId']=re['access']['token']['id']
        r['expires']=datetime.datetime.strptime(re['access']['token']['expires'],'%Y-%m-%dT%H:%M:%SZ')
        r['tenantId']=re['access']['token']['tenant']['id']
        serviceCatalog={}
        for sc in re['access']['serviceCatalog']:
            serviceCatalog[sc['name']]=sc['endpoints'][0]['publicURL']
        r['serviceCatalog']=serviceCatalog
        return r
    else:
        print result.status_code
        print result.raw