from fabric.api import *
import os
import os.path
import time

bkuptime=time.strftime("%Y%m%d-%H%M%S", time.localtime())

def mkdir(**js):
 path=js["path"]
 parentdir=os.path.dirname(path)
 run("ls -ld %(parentdir)s" % locals() )
 run("mkdir -m %(mode)s %(path)s" % js)

def filetransfer(**js):
 if (js["srcserver"]=="localhost"):
  # -H dstserver
  put(js["srcpath"],js["dstpath"])
  run("chmod %(mode)s %(dstpath)s" % js)
  sudo("chown %(owner)s:%(group)s %(dstpath)s" % js)
 elif (js["dstserver"]=="localhost"):
  # -H srcserver
  get(js["srcpath"], js["dstpath"])
 else:
  # use remote->local, local->remote when remote->remote
  raise Exception, "Please Define localhost"


def execshell(**js):
 run("ls -ld %(path)s" % js )
 run("%(path)s" % js)

def editat(**js):
 operation=js["operation"]
 if (operation=="add"):
  datestring="%(hour)s:%(minute)s %(year)s-%(month)s-%(day)s" % js
  run("echo %s | at '%s'" % (js["command"], datestring))
 else:
  raise Exception

def passwdresetos(username):
 sudo("faillog -u %(username)s -r")

def deletefile(**js):
 run("rm -f %(filepath)s" % js)

def editcron(**js):
 cronline="%(minute)s %(hour)s %(day)s %(month)s %(dayofweek)s " % js
 osname=run("uname")
 if (osname=="AIX"):
  tmp="su - %(user) %(command)s" % js
  crontabdir='/var/spool/cron/crontabs/'
 elif (osname=="Linux"):
  checkdistrib=run("ls /etc/*-release | grep SuSE | wc -l")
  if (checkdistrib=="1"):
   crontabdir='/var/spool/cron/tabs/'
  elif (checkdistrib=="0"):
   crontabdir='/var/spool/cron/'
  else:
   raise Exception, "Distribution check failed"
  tmp='su - %(user)s -c "%(command)s"' % js
 cronline += tmp
 sudo("if [[ ! -d %(crontabdir)s/backup ]]; then mkdir %(crontabdir)s/backup; fi" % locals())
 sudo("cp -fp %s/root %s/backup/root.%s" % (crontabdir, crontabdir, bkuptime))
 if (js["operation"]=="add"):
  sudo("echo '%(cronline)s' >> %(crontabdir)s/root_active" % locals())
  sudo("crontab %(crontabdir)s/root_active" % locals())
 elif (js["operation"]=="del"):
  sudo("grep -v '%(cronline)s' %(crontabdir)s/root > /tmp/roottmp" % locals())
  sudo("cp -fp /tmp/roottmp %(crontabdir)s/root_active" % locals())
  sudo("crontab %(crontabdir)s/root_active" % locals())
 else:
  raise Exception

def mountnfs_exportfs(**js):
 sudo("mkdir -p /etc/backup/")
 sudo("cp -fp /etc/exports /etc/backup/exports.%s" % bkuptime)
 exportsline="%(exportpath)s %(servername)s(rw)" % js
 if (js["operation"]=="add"):
  sudo("echo '%s' >> /etc/exports" % exportsline)
  sudo("exportfs -a")
 elif (js["operation"]=="del"):
  sudo("grep -v '%s' /etc/exports > /tmp/exportstmp" % exportsline)
  sudo("cp -fp /tmp/exportstmp /etc/exports")
  sudo("exportfs -r")

def mountnfs(**js):
 if(js["mountoption"]==""):
  js["mountoption"]="hard,intr"
 sudo("mkdir -p /etc/backup/")
 sudo("cp -fp /etc/fstab /etc/backup/fstab.%s" % bkuptime)
 fstabline="%(nfsserver)s:%(exportpath)s %(mountpoint)s nfs %(mountoption)s 0 0" % js
 if (js["operation"]=="add"):
  sudo("echo %s >> /etc/fstab" % fstabline)
  sudo("mount %(mountpoint)s" % js)
 elif (js["operation"]=="del"):
  sudo("umount %(mountpoint)s" % js)
  sudo("grep -v '%s' /etc/fstab > /tmp/fstabtmp" % fstabline)
  sudo("cp -fp /tmp/fstabtmp /etc/fstab")
 else:
  raise Exception, "unknown operation: %s" % operation

def modifydns(**js):
 domainname=".".join(js["fqdn"].split(".")[1:])
 sudo("mkdir -p /var/named/backup/")
 sudo("cp -fp /var/named/data/%s /var/named/backup/%s.%s" % (domainname,domainname,bkuptime))
 # determine ipaddr zone file:
 ipaddr=js["ipaddr"]
 ptrzone=".".join(ipaddr.split(".")[:-1])
 #print ptrzone
 tmp=sudo("ls /var/named/data/%(ptrzone)s* | head -n 1" % locals())
 ptrzonefile=os.path.basename(tmp)
 #print ptrzonefile
 sudo("cp -ip /var/named/data/%s /var/named/backup/%s.%s" % (ptrzonefile,ptrzonefile,bkuptime))
 tmp=ipaddr.split(".")
 tmp.reverse()
 tmp.extend(["in-addr.arpa."])
 #print tmp
 reversedipaddr=".".join(tmp)
 #print reversedipaddr
 # zone file:
 bindaline="%(fqdn)s. IN A %(ipaddr)s" % js
 bindptrline="%s IN PTR %s." % (reversedipaddr, js["fqdn"])
 if (js["operation"]=="add"):
  sudo("echo %s >> /var/named/data/%s" %(bindaline , domainname))
  sudo("echo %s >> /var/named/data/%s" %(bindptrline , ptrzonefile))
  sudo("service named reload" % js)
 elif (js["operation"]=="del"):
  sudo("grep -v '%s' /var/named/data/%s > /tmp/namedzonetmp" % (bindaline, domainname))
  sudo("cp -fp /tmp/namedzonetmp /var/named/data/%(domainname)s" % locals())
  sudo("grep -v '%s' /var/named/data/%s > /tmp/namedzonetmp" % (bindptrline, ptrzonefile))
  sudo("cp -fp /tmp/namedzonetmp /var/named/data/%(ptrzonefile)s" % locals())
  sudo("service named reload" % js)
 else:
  raise Exception, "unknown operation: %s" % operation

def execsql(**js):
 pass

def modifyuseros(**js):
 if (js["operation"]=="add"):
  pgrp=js["groups"].split(',')[0]
  js["pgrp"]=pgrp
  sudo ('useradd -g %(pgrp) -G %(groups)s %(username)' % js)
 elif (js["operation"]=="del"):
  sudo ('userdel -r %(username)' % js)
 else:
  raise Exception

def setpublickey(**js):
 env.user=js["username"]
 env.password=js["password"]
 publickey_text=os.popen('cat ~/.ssh/id_rsa.pub').read()
 run ('mkdir .ssh')
 run ('chmod 700 .ssh')
 run ("echo '{0}' >> .ssh/authorized_keys".format(publickey_text))
 run ("chmod 600 .ssh/authorized_keys")
