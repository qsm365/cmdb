#!/bin/bash
cn=$1
wget -q -O /opt/cmdb/enc_yaml/$1.yaml http://127.0.0.1/cmdb/enc?certname=$cn
cat /opt/cmdb/enc_yaml/$1.yaml
