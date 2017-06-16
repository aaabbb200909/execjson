#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import subprocess
import sys
import json
import glob
import threading
import time
import os

###
dryrun=True
#dryrun=False
#
generic_parse_list=["mkdir", "execshell", "editcron", "editat", "deletefile",
"modifyuseros", "passwdresetos", "setpublickey"
]
###
finallyjobidlist=[] #global
timeformat="%Y/%m/%d %H:%M" # const
timeformatwithsec=timeformat+":%S" # const
def getcurrenttime():
 return time.strftime(timeformatwithsec, time.localtime())

class CommandExecException(Exception):
 pass

def uploadjsontoelasticsearch(jsonstr, filename):
 docid=os.path.basename(filename)
 elasticsearchurl='localhost:9200'
 os.popen('curl --silent --max-time 15 -XPUT http://%s/jobstates/jobstate/%s -d @%s.state > /dev/null' % (elasticsearchurl, docid, filename)) # hmm..

def dumpstatejson(dictforjs, filename):
 js=json.dumps(dictforjs, indent=4)
 with open(filename+".state", "w") as f:
  f.write(js)
 t=threading.Thread(target=uploadjsontoelasticsearch, args=[js, filename])
 t.start()

def printsubprocessstdout(p): 
 st=p.stdout.readline()
 while (st):
  try:
   tmp=st.decode('Shift-JIS')
  except UnicodeDecodeError as e:
   tmp=st
  sys.stdout.write(tmp)
  st=p.stdout.readline() 

def exec_or_dryrun(cmdstring, slowjobthreshold=600):
 if (dryrun):
  print cmdstring
 else:
  subprocessargs={ 'stdout': subprocess.PIPE, 'stderr': subprocess.STDOUT, 'shell': True}
  p = subprocess.Popen(cmdstring, **subprocessargs)
  t=threading.Thread(target=printsubprocessstdout, args=[p])
  t.start()
  starttime=time.time()
  while (p.poll() == None):
   if (starttime + slowjobthreshold < time.time()):
    print "this job seems a bit slow: %s" % cmdstring
   sys.stdout.flush()
   time.sleep(5)
  if (p.returncode != 0):
   raise CommandExecException, cmdstring
  else:
   pass

def create_fabdict(args):
 # "args" should be dict
 tmp=["%s='%s'" %(k,args[k]) for k in args]
 return ",".join(tmp)


def parse_filetransfer(listargs):
 for js in listargs:
   if (js["srcserver"]=="localhost"):
    print exec_or_dryrun(
     "fab -H %s filetransfer:%s" % (js["dstserver"], create_fabdict(js))
    )
   elif (js["dstserver"]=="localhost"):
    print exec_or_dryrun(
     "fab -H %s filetransfer:%s" % (js["srcserver"], create_fabdict(js))
    )
   else:
    origdstserver=js["dstserver"]
    js["dstserver"]="localhost"
    print exec_or_dryrun(
     "fab -H %s filetransfer:%s" % (js["srcserver"], create_fabdict(js))
    )
    js["dstserver"]=origdstserver
    js["srcserver"]="localhost"
    print exec_or_dryrun(
     "fab -H %s filetransfer:%s" % (js["dstserver"], create_fabdict(js))
    )

def generic_parse(listargs, command, hoststring="server"):
 for js in listargs:
  print exec_or_dryrun(
   "fab -H %s %s:%s" % (js[hoststring], command, create_fabdict(js))
  )

def parse_mountnfs(listargs):
 for js in listargs:
  print exec_or_dryrun(
   "fab -H %s mountnfs_exportfs:%s" % (js["nfsserver"], create_fabdict(js))
  )
  print exec_or_dryrun(
   "fab -H %s mountnfs:%s" % (js["servername"], create_fabdict(js))
  )

def parse_modifydns(listargs):
 pass

def parse_others(listargs):
 raise CommandExecException, "Please do other work, and come here again: %s" % (repr(listargs))

def parse_sleepandexception(listargs):
 js=listargs[0] # always 1 operation
 try:
  sleeptime=int(js["sleep"])
 except ValueError as e:
  sleeptime=0
 #print sleeptime
 time.sleep(sleeptime)
 if (js["exception"]=="yes"):
  raise CommandExecException, "Exception Test"
 else:
  print "No Exception Test"

def doparse(job, myparalleljobstate=None, paralleljobstatelist=None):
  name=job["name"]
  listargs=job["args"]
  jobtime=job["time"]
  if (not (jobtime == None or jobtime == "")):
   jobtime=time.strptime(jobtime, "%Y/%m/%d %H:%M")
  #print jobtime
  iffail=job["iffail"]
  id=job["id"]

  # if jobtime is set, wait for a bit:
  if (not jobtime == ""):
   while (jobtime > time.localtime()):
    print time.localtime()
    time.sleep(60)

  try:
   if (name in generic_parse_list):
    generic_parse(listargs, name)
   elif (name=="filetransfer"):
    parse_filetransfer(listargs)
   elif (name=="mountnfs"):
    parse_mountnfs(listargs)
   elif (name=="modifydns"):
    parse_modifydns(listargs)
   elif (name=="others"):
    parse_others(listargs)
   elif (name=="sleepandexception"):
    parse_sleepandexception(listargs)
   elif (name=="waitparalleljob"):
    if (len(paralleljobstatelist) != 0): # always True
     for t in [x.thread for x in paralleljobstatelist]:
      t.join()
    for p in paralleljobstatelist:
     if (not p.exception == None):
      if (p.iffail=="stop"):
       raise CommandExecException, "Parallel Job gave me Exception. Check the log for detail"
      else:
       print "Parallel Job gave me Exception. Go on."
   else:
    print job
  except CommandExecException as e:
    print e
    if (not myparalleljobstate == None):
     myparalleljobstate.exception=e
    if (iffail == "stop" or name=="others"):
     # if sortofop is "others", always stop here:
     job["state"]="abended"
     raise e
    elif (iffail == "go"):
     pass
    else:
     finallyjobidlist.append(iffail)

# http://stackoverflow.com/questions/2829329/catch-a-threads-exception-in-the-caller-thread-in-python
class paralleljobstate:
 def __init__(s):
  s.id=None
  s.iffail=""
  s.thread=None
  s.exception=None

def createjob(name, id, time, iffail, args, state):
 job={
  "name": name,
  "id": id,
  "time": time,
  "iffail": iffail,
  "args": args,
  "state": state
 }
 return job


def parse(dictforjs, filename):
 joblist=dictforjs["joblist"]
 paralelljobidlist=[]
 paralleljobstatelist=[]

 # precheck loop:
 runtimeaddjoblist=[] # [[pos, job], [pos, job], ..] 
 for i in range(len(joblist)):
  job=joblist[i]

  # check parallel jobs, etc:
  if(i > 0):
   if (job["id"] == joblist[i-1]["id"]):
    paralelljobidlist.append(job["id"])
    if (i < len(joblist)-1):
     if (job["id"] == joblist[i+1]["id"]):
      pass
     else:
      runtimeaddjoblist.append([i+1, createjob("waitparalleljob", "-1", "", "stop", {}, "notyet")])

  # set all jobs: state notyet
  if (not "state" in job):
   job["state"]="notyet"

 # Add runtime job now:
 for positionjob in runtimeaddjoblist:
  joblist.insert(positionjob[0], positionjob[1])

 # Save what we have done:
 dumpstatejson(dictforjs, filename)

 # main loop:
 for job in joblist:
  #print(finallyjobidlist)
  if (not len(finallyjobidlist)==0 and not job["id"] in finallyjobidlist):
   continue
  #print job
  if (job["state"]=="done"):
   continue
  job["state"]="ongoing"
  job["starttime"]=getcurrenttime()
  dumpstatejson(dictforjs, filename)
  if(job["id"] in paralelljobidlist):
   #print("parallel job")
   myparalleljobstate=paralleljobstate()
   t=threading.Thread(target=doparse,args=[job, myparalleljobstate])
   t.start()
   #
   myparalleljobstate.thread=t
   myparalleljobstate.iffail=job["iffail"]
   paralleljobstatelist.append(myparalleljobstate)
  else:
   #print("normal job")
   try:
    if (job["name"]=="waitparalleljob"):
     doparse(job, paralleljobstatelist=paralleljobstatelist)
    else:
     doparse(job)
    job["state"]="done"
   finally:
    job["endtime"]=getcurrenttime()
    dumpstatejson(dictforjs, filename)


## Main:
if __name__ == '__main__':
 if (len(sys.argv)!=2):
  print "Usage do.py jsonfilename"
  sys.exit(31)
 filename=sys.argv[1]
 if (os.path.exists(filename+".state")):
  print u"stateファイルが存在しています"
  raise Exception
 
 with open(filename) as f:
  dictforjs=json.loads(f.read())
 jobenvcode=dictforjs["jobenvcode"] # Global
 jobapplcode=dictforjs["jobapplcode"] # Global
 dictforjs["@timestamp"]=getcurrenttime()
 #print joblist
 parse(dictforjs, filename)

