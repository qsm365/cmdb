# cmdb
> a cmdb based on python and Django</br>
> i also add some extension function to support configuration and application manager</br>

### Configuration Manager
> this function is based on puppet </br>
> the cmdb can manage the puppet module,and work as a "External Node Classifier"</br>
> you can just add the enc.sh to your puppet master server,and change your puppet config file to use it

### Application Manager
> this function is based on docker and docker registry</br>
> the cmdb can show the docker containers on the server and the image in the docker registry, </br>
> and also show the detail of the container through the docker engine api

### Dependency:
> Django (1.8.1)</br>
> MySQL-python (1.2.5)</br>
> PyYAML (3.11)</br>
> PIL (1.1.6) --with freetype</br>
> docker-py (1.2.3)</br>
> requests (2.5.2)</br>
> backports.ssl_match_hostname (3.4.0.2)</br>
> websocket_client (0.32.0)</br>
> python-openstackclient (2.2.0)</br>
> python-dateutil (2.5.1)</br>

### UI Priview:
![3](https://raw.github.com/qsm365/cmdb/master/preview/3.png "the host list")</br></br>
![4](https://raw.github.com/qsm365/cmdb/master/preview/4.png "the host detail")</br></br>
![1](https://raw.github.com/qsm365/cmdb/master/preview/1.png "the application(docker) module")</br></br>
![2](https://raw.github.com/qsm365/cmdb/master/preview/2.png "the image(docker image) module")</br></br>
