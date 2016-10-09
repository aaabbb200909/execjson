# execjson
Service Request should be written in JSON

#Getting Started

When you receive Service Request from your customer, I expect most often you receive e-mail (free format) or Excel/Word form, especially, when you need an approver for your request on your own Request Handling system, such as IBM Notes or Sharepoint.

Unfortunately, both of e-mail and Excel/Word is not easy to parse compared to web form.

To overcome this constraint, execjson will create JSON from Web form, which could go through your approver, and also will be imported to your Web form again.

It is also able to dispatch successive or parallel job, based on your JSON.


#Install

You need to setup Django to install execjson.
- prefered setting: Centos7, Django1.6(EPEL)

- Currently, I haven't yet updated to Django 1.10

~~~~
    $ cd /var/tmp && git clone git@github.com:aaabbb200909/execjson.git
    $ cd /var/tmp/execjson/web/mysite
    $ ./manage.py syncdb (Create SessionDB)
    $ ./manage.py runserver (Start WebServer)
    $ cd /var/tmp/execjson/web/mysite/batch/ && ./do.sh (Start job dispatcher)
~~~~

#Reference
author's blog (written in Japanese)
http://aaabbb-200904.hatenablog.jp/archive/category/execjson
