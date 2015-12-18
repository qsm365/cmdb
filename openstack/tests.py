from django.test import TestCase
from openstack import identityapi

# Create your tests here.
if __name__=='__main__':
    print "test authenticate"
    r=identityapi.authenticate('40.40.40.187',5000,'admin','admin','secrete')
    print r['tokenId']
    print r['expires']
    print r['tenantId']
    tokenid=r['tokenId']
    #print r['serviceCatalog']
    if r['serviceCatalog']['nova']:
        uri=r['serviceCatalog']['nova']
        #ss = nova.listServers(uri,tokenid)
        #print nova.serverDetail(uri,ss[0]['id'],tokenid)
        #fid = nova.createFlavor(uri,'api',1,64,64,1,tokenid)
        #nova.deleteFlavor(uri,'f5a9eff3-3694-4090-8d37-c400bde82aaf',tokenid)
        #ff = nova.listFlavors(uri,tokenid)
        #for f in ff.items():
        #    print nova.flavorDetail(uri, f[0], tokenid)
        #print nova.importKeypair(uri, 'test', 'blabla', tokenid)
        #kk = nova.listKeypairs(uri,tokenid)
        #print nova.keypairDetail(uri,kk[0]['name'],tokenid)
        #nova.deleteKeypair(uri, kk[0]['name'], tokenid)
        #print nova.createNetwork(uri, "test", "192.168.3.128/24", tokenid,dns1='114.114.114.114')
        #nn = nova.listNetwork(uri, tokenid)
        #print nova.networkDetail(uri, nn[0]['id'], tokenid)
        #print nova.deleteNetwork(uri, nn[0]['id'], tokenid)
        #print nova.reserveIp(uri, "192.168.3.150", tokenid)
        #name='vm3'
        #flavorid='3f09acbe-07c6-4280-b1d4-a38e0afc43ad'
        #volumeid='52afc0dc-a0c5-47e6-b6b7-e65d31dc1dc7'
        #networkid='4d95cd35-52a5-436d-8d9f-50d4f4273487'
        #fixip='40.40.40.3'
        #keyname='admin-key'
        #print nova.createServer(uri,name,flavorid,volumeid,networkid,fixip,keyname,tokenid)
    if r['serviceCatalog']['cinderv2']:
        uri=r['serviceCatalog']['cinderv2']
        #print cinder.createVolume(uri, 'vm3-vol', 10, tokenid,imageRef='b9df73e0-d5b1-44ac-8bdf-ec8863bd9874')
        #cc = cinder.listVolumes(uri,tokenid)
        #print cinder.volumeDetail(uri, cc[0]['id'], tokenid)
        #print cinder.deleteVolume(uri, cc[0]['id'], tokenid)
    if r['serviceCatalog']['glance']:
        uri=r['serviceCatalog']['glance']
        #print glance.createImage(uri, "test", "bare", "raw", tokenid)
        #gg = glance.listImages(uri, tokenid)
        #print gg[1]['id']
        #print glance.ImageDetail(uri, gg[0]['id'], tokenid)