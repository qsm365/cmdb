# cmdb
>a cmdb based on python and Django
>i also add some extension function to support configuration and application manager

### Configuration Manager
>this function is based on puppet
>the cmdb can manage the puppet module,and work as a "External Node Classifier"
>you can just add the enc.sh to your puppet master server,and change your puppet config file to use it

### Application Manager
>this function is based on docker
>the cmdb can show the docker containers on the server, 
>and also show the detail of the container through the docker engine api

### Dependency:
> Django (1.8.1)
> MySQL-python (1.2.5)
> PyYAML (3.11)
> PIL (1.1.6) --with freetype and jpeg
> docker-py (1.2.3)
> requests (2.5.2)
> backports.ssl_match_hostname (3.4.0.2)
> websocket_client (0.32.0)

### UI Priview:
![github](http://github.com/qsm365/cmdb/master/preview/1.png "preview1")
![github](http://github.com/qsm365/cmdb/master/preview/2.png "preview2")
![github](http://github.com/qsm365/cmdb/master/preview/3.png "preview3")
![github](http://github.com/qsm365/cmdb/master/preview/4.png "preview4")