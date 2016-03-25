from novaclient import client

api_ver = '2'
auth_url='http://controller:5000/v2.0'
tenant='admin'
user='admin'
passwd='asdf3.14'

def listInstances():
    nc = client.Client(api_ver, user, passwd, tenant,
                       auth_url, connection_pool=True)
    r=[]
    for server in list(nc.servers.list()):
        s=translateServer(server);
        r.append(s)
    return r

def showInstances(instanceId):
    nc = client.Client(api_ver, user, passwd, tenant,
                       auth_url, connection_pool=True)
    server = nc.servers.get(instanceId)
    return translateServer(server);

def translateServer(server):
    s = server.to_dict();
    s['hypervisor'] = s['OS-EXT-SRV-ATTR:host']
    return s

def getFlavor(instanceId):
    nc = client.Client(api_ver, user, passwd, tenant,
                       auth_url, connection_pool=True)
    flavor = nc.flavors.get(instanceId)
    return flavor.to_dict()