# execjson
Service Request should be written in JSON

# Getting Started

When you receive Service Request from your customer, I expect most often you receive an e-mail like plain text or Excel/Word form, especially, when you have your own ITIL system (like OTRS) .

Unfortunately, both of e-mail and Excel/Word is not structured data and not easy to parse.

To overcome this constraint, execjson will create JSON from Web form, which could go through your ITIL system, and also will be imported to your Web form again.

It is also able to dispatch serial or parallel job, based on your JSON.


# Install

You need to setup Django to install execjson.
- prefered setting: Django1.10

~~~~
    $ cd /var/tmp && git clone git@github.com:aaabbb200909/execjson.git
    $ cd /var/tmp/execjson/web/mysite
    $ ./manage.py migrate (Create SessionDB)
    $ ./manage.py compilemessages (Create Translation)
    $ ./manage.py runserver (Start WebServer)
then access this url:
http://localhost:8000/app1/
    $ cd /var/tmp/execjson/web/mysite/batch/ && ./do.sh (Start job dispatcher)
~~~~

or you can use docker
~~~~
$ sudo docker run -d -p 8000:8000 tnaganawa/execjson
~~~~

# Usage
https://github.com/aaabbb200909/execjson/wiki

# Reference
author's blog (written in Japanese)  
http://aaabbb-200904.hatenablog.jp/archive/category/execjson
