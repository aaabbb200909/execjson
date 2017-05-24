FROM centos:7
RUN yum install -y python-setuptools git gettext httpd && easy_install pip && pip install -U django python-gettext django-debug-toolbar && cd /opt && git clone https://github.com/tnaganawa/execjson.git && cd /opt/execjson/web/mysite/ && ./manage.py migrate && ./manage.py compilemessages
EXPOSE 8000
CMD ["/bin/bash", "-c", "cd /opt/execjson; ./entrypoint.sh"]
