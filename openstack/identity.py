import requests
import json
import datetime
import nova
import cinder
import glance

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
    
if __name__=='__main__':
    print "test authenticate"
    r=authenticate('192.168.3.9',5000,'admin','admin','secrete')
    print r['tokenId']
    print r['expires']
    print r['tenantId']
    tokenid=r['tokenId']
    #print r['serviceCatalog']
    if r['serviceCatalog']['nova']:
        uri=r['serviceCatalog']['nova']
        #ss = nova.listServers(uri,tokenid)
        #fid = nova.createFlavor(uri,'api',1,64,64,1,tokenid)
        #nova.deleteFlavor(uri,'f5a9eff3-3694-4090-8d37-c400bde82aaf',tokenid)
        #ff = nova.listFlavors(uri,tokenid)
        #for f in ff.items():
        #    print nova.flavorDetail(uri, f[0], tokenid)
        #print nova.importKeypair(uri, 'test', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCaklw+wN6Ytktj9jUaHeDEZ/6nxCi/SDahWTEayHTKfarGwywvwsYs8yYuB3LHnU0FKlkCb/+8baZ+uPd2ISnU3U8TBfPg5C8A4Ab2Haz+HoMIs/2ySkXfgmW+l8se3NB5xe7ZqR1FgYWdJJ78puhIw9K42dR+Mej7GnLpsP1HrxVbloMRcBjfORFPMmJBQmyVg1GotON7wv303lbb5HdV3/WZJridjOY3EYEU0wXKQtGtWt+QmYlxJvKJrHDXTlpHSPaQ2Yi+9m+8a8kkqHnmKjHbN2u9bi6A+daMMYmlnffWDRgkmGokTxGF0QVjo9WfhxIy5kXYyuySI2S+lVWR Generated-by-Nova', tokenid)
        #kk = nova.listKeypairs(uri,tokenid)
        #print nova.keypairDetail(uri,kk[0]['name'],tokenid)
        #nova.deleteKeypair(uri, kk[0]['name'], tokenid)
        #print nova.createNetwork(uri, "test", "192.168.3.128/24", tokenid,dns1='114.114.114.114')
        #nn = nova.listNetwork(uri, tokenid)
        #print nova.networkDetail(uri, nn[0]['id'], tokenid)
        #print nova.deleteNetwork(uri, nn[0]['id'], tokenid)
        #print nova.reserveIp(uri, "192.168.3.150", tokenid)
    if r['serviceCatalog']['cinderv2']:
        uri=r['serviceCatalog']['cinderv2']
        #print cinder.createVolume(uri, 'test', 1, tokenid,imageRef='a1ece8da-be39-4de9-b111-bb9416dd4487')
        #cc = cinder.listVolumes(uri,tokenid)
        #print cinder.volumeDetail(uri, cc[0]['id'], tokenid)
        #print cinder.deleteVolume(uri, cc[0]['id'], tokenid)
    if r['serviceCatalog']['glance']:
        uri=r['serviceCatalog']['glance']
        print glance.createImage(uri, "test", "bare", "raw", tokenid)
        #gg = glance.listImages(uri, tokenid)
        #print gg[1]['id']
        #print glance.ImageDetail(uri, gg[0]['id'], tokenid)