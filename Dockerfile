FROM centos:7
RUN yum install -y python-setuptools git gettext httpd mod_wsgi gcc python-devel openssl-devel libffi-devel && easy_install pip && pip install -U django python-gettext fabric && cd /opt && git clone https://github.com/tnaganawa/execjson.git && cd /opt/execjson/web/mysite/ && ./manage.py migrate && ./manage.py compilemessages && chown -R apache.apache /opt/execjson
RUN mkdir /var/www/html/execjson && mkdir /var/www/html/execjson/user1 && mkdir /var/www/html/execjson/user2 && htpasswd -bc /etc/httpd/conf/.htpasswd user1 user1 && htpasswd -b /etc/httpd/conf/.htpasswd user2 user2
COPY docker/execjson.conf /etc/httpd/conf.d/
EXPOSE 8000 80
CMD ["/bin/bash", "-c", "cd /opt/execjson; ./entrypoint.sh"]
