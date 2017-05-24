#!/bin/bash
cd /var/tmp/execjson/web/mysite/batch
./do.sh &
cd /var/tmp/execjson/web/mysite
./manage.py runserver 0.0.0.0:8000
