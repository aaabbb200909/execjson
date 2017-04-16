FROM centos:7
RUN yum install -y python-setuptools git gettext && easy_install pip && pip install -U django python-gettext && cd /opt && git clone https://github.com/tnaganawa/execjson.git && cd /opt/execjson/web/mysite/ && ./manage.py migrate && ./manage.py compilemessages
EXPOSE 8000
CMD ["/opt/execjson/web/mysite/manage.py", "runserver", "0.0.0.0:8000"]
