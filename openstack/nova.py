import novaapi
import identityapi

ksIP=''
ksPort=''
tenant=''
user=''
passwd=''

def listInstances():
    r=identityapi.authenticate(ksIP, ksPort, tenant, user, passwd)
    if r:
        tokenid=r['tokenId']
        if r['serviceCatalog']['nova']:
            uri=r['serviceCatalog']['nova']
            servers=novaapi.listServers(uri, tokenid)
            return servers
        
def listInstancesByHV(hv):
    r=identityapi.authenticate(ksIP, ksPort, tenant, user, passwd)
    if r:
        tokenid=r['tokenId']
        if r['serviceCatalog']['nova']:
            uri=r['serviceCatalog']['nova']
            servers=novaapi.listServers(uri, tokenid)
            result=[]
            for server in servers:
                if server['hv']==hv:
                    result.append(server)
            return result
        
def show(vmid):
    r=identityapi.authenticate(ksIP, ksPort, tenant, user, passwd)
    if r:
        tokenid=r['tokenId']
        if r['serviceCatalog']['nova']:
            uri=r['serviceCatalog']['nova']
            servers=novaapi.serverDetail(uri, vmid, tokenid)
            return servers