#!/bin/bash
httpd
#
mkdir -m 700 ~/.ssh
ssh-keygen -N '' -f ~/.ssh/id_rsa
#
cd /opt/execjson/web/mysite/batch
./do.sh
