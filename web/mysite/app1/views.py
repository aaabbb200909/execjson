# -*- coding: utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response,render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.translation import ugettext as _
from app1.models import user_id_jsons
import app1.settings as settings
import json
import re
import time
import os

###
operationswithseveralops=settings.operationswithseveralops
jsondir=settings.jsondir

def get_user(request):
 user=None
 if (request.META.has_key('HTTP_X_FORWARDED_USER')):
  user=request.META['HTTP_X_FORWARDED_USER']
 elif (request.META.has_key('REMOTE_USER')):
  user=request.META['REMOTE_USER']
 #print (user)
 return user

def get_authorization(request):
 if (settings.use_authorization == False):
  return 'opsuser' # authorization feature disabled
 user=get_user(request)
 if user in settings.role_opsusers:
  return 'opsuser'
 elif user in settings.role_applusers:
  return 'appluser'
 elif user in settings.role_managers:
  return 'manager'
 return 'normaluser'


class jsonpair():
 def __init__(s, jsonfilename, jsonbody, jsonsummary):
  s.jsonfilename=jsonfilename
  s.jsonbody=jsonbody
  s.jsonlogname=os.path.basename(jsonfilename+'.txt')
  s.jsonsummary=jsonsummary


@csrf_protect
def dashboard(request):
 role=get_authorization(request)
 if (role != 'opsuser'):
  return HttpResponse("You are not authorized.")
 # Get working json:
 l=os.popen("ps -u apache -o args | grep -v grep | grep do.py | awk '{print $NF;}'").readlines()
 l=[st.rstrip() for st in l]
 jsonpairs=[]
 jsonsummaries=[]
 for jsonfilename in l:
  with open(jsonfilename+".state") as f:
   js=json.load(f)
  jsonsummary=[ 
   {"jobenvcode": js["jobenvcode"], 
    "jobapplcode": js["jobapplcode"],
    "@timestamp": js["@timestamp"],
    "numofjobs": len(js["joblist"]),
   }
  ]
  jsonpairs+=[jsonpair(jsonfilename, json.dumps(js, indent=4), repr(jsonsummary))]
 return render(request, 'dashboard.html', {"jsonsummaries": jsonsummaries, "jsonpairs":jsonpairs})


def createmultiopjs():
 multiopjs= 'var multioplist={'
 for op in operationswithseveralops:
  multiopjs+='"%s":1, ' % op
 multiopjs=multiopjs[:-2] # remove final ', '
 multiopjs+='};'
 return multiopjs


@csrf_exempt
def index(request):
    user=get_user(request)
    role=get_authorization(request)
    joblist=[]
    dictforjs={}
    if ("dictforjs" in request.session):
     dictforjs=request.session['dictforjs']
    #print (dictforjs)

    # Create javascript to set session:
    tmp=""
    if ("jobenvcode" in dictforjs):
     tmp += '$("#jobenvcode").val("%s");' % dictforjs["jobenvcode"]
    if ("jobapplcode" in dictforjs):
     tmp += '$("#jobapplcode").val("%s");' % dictforjs["jobapplcode"]
    if ("joblist" in dictforjs):
     joblist=dictforjs["joblist"]
    for job in joblist:
     tmp+='addjob("%s","%s","%s","%s", "%s");' % (job["name"],job["id"],job["time"],job["iffail"], len(job["args"]) )
     for i in range(len(job["args"])):
      for k in job["args"][i].keys():
       tmp+='$("[name=%s]").eq(%s).val( "%s" );' % (k, i-len(job["args"]), job["args"][i][k])

    # create multioplist
    tmp += createmultiopjs()
    #print (tmp)

    return render(request, 'index.html', {"joblist":joblist, "sessionjs": tmp, "role": role, "user": user, "settings": settings} )


def pop_evenif_not_list(list_or_not):
 if (type(list_or_not)==list):
  return list_or_not.pop(0)
 else:
  return list_or_not

def consume(duprp, arglist):
 tmp={}
 for k in arglist:
  #print duprp[k]
  tmp[k]=pop_evenif_not_list(duprp.getlist(k))
 return tmp

def consumeoperationargs(jobname, duprp):
 for job in settings.jobs:
  if (jobname==job["jobname"]):
   return consume(duprp, job["args"])
 if (jobname=="others"):
  return consume(duprp, ["filename"])
 elif (jobname=="sleepandexception"):
  return consume(duprp, ["sleep", "exception"])


@csrf_exempt
def load(request):
    rp=request.POST
    #print (rp)
    loadjson=request.FILES["putjson"].read() # hmm..
    #print (loadjson)
    dictforjs=json.loads(loadjson)
    # print (dictforjs)
    request.session["dictforjs"]=dictforjs
    return redirect(index)


@csrf_protect
def dbsave(request):
    user=get_user(request)
    if (user == None):
      raise Exception("anonymous user can't use dbsave")
    dictforjs = request.session["dictforjs"]
    savejson=json.dumps(dictforjs)
    savedata=user_id_jsons(user=user, saveid='1', json=savejson, state='saved')
    savedata.save()
    return redirect(index)

@csrf_protect
def dbload(request):
    user=get_user(request)
    role=get_authorization(request)
    if (user == None):
      raise Exception("anonymous user can't use dbload")
    rp=request.POST
    if (role == 'manager'):
      dbloaduser=rp.get('dbuser')
    elif (role == 'opsuser'):
      dbloaduser=rp.get('dbuser')
      if (user_id_jsons.objects.get(user=dbloaduser, saveid='1').state != "approved"):
        raise Exception("since this SR is not approved yet, i can't load this")
    else:
      dbloaduser=user
    loadjson=user_id_jsons.objects.get(user=dbloaduser, saveid='1').json
    dictforjs=json.loads(loadjson)
    request.session["dictforjs"]=dictforjs
    if (role == 'manager'):
      if ('dbapprove' in rp):
        dbuserjson=user_id_jsons.objects.get(user=dbloaduser, saveid='1')
        dbuserjson.state='approved'
        dbuserjson.save()
    return redirect(index)

@csrf_protect
def clearcache(request):
    # GET allows easy SessionReset ..
    if  ('dictforjs' in request.session):
     tmp=request.session['dictforjs']
     del request.session['dictforjs']
    return redirect(index)


@csrf_protect
def createjson(request):
    role=get_authorization(request)
    rp=request.POST
    duprp=rp.copy() # Consume all the tokens with consume_xxx methods
    #print (duprp)

    ids=rp.getlist('id')
    for id in ids:
     tmp=re.match(r"\d+", id)
     if (tmp == None):
      return HttpResponse(_("non numeric caracter is used in an ID: ")+repr(id))
    jobtimes=rp.getlist('time')
    for jobtime in jobtimes:
     if (jobtime == ""):
      continue
     try:
      time.strptime(jobtime, "%Y/%m/%d %H:%M")
     except ValueError as e:
      return HttpResponse(_("incorrect time format:")+repr(jobtime))
    iffails=rp.getlist('iffail')
    for iffail in iffails:
     tmp=re.match(r"[\d,]+\d", iffail)
     if (not iffail in ('stop', 'go') and tmp == None):
      return HttpResponse(_("iffail contailns invalid value: stop/go, or ID cound be used:")+repr(iffail))
    operations=rp.getlist('name')

    import itertools
    names=[]
    numsofnames=[]
    for k,g in itertools.groupby(operations):
     tmp=len(list(g))
     if(k in operationswithseveralops):
      numsofnames.append(tmp)
      names.append(k)
     else:
      # "others" etc, always should be single op:
      for i in range(tmp):
       numsofnames.append(1)
       names.append(k)

    #print ids, names
    if(not len(ids) == len(names)):
     #raise Exception
     return HttpResponse(_("number of Job and number of Operation is different"))

    # Begin consume:
    jobenvcode=rp.getlist('jobenvcode')[0]
    jobapplcode=rp.getlist('jobapplcode')[0]
    joblist=[]
    dictforjs={"jobenvcode": jobenvcode, "jobapplcode": jobapplcode, "joblist": joblist}
    #print duprp
    for i in range(len(jobtimes)):
     job={}
     job["id"]=ids[i]
     job["name"]=names[i]
     job["time"]=jobtimes[i]
     job["iffail"]=iffails[i]
     job["args"]=[]
     for i in range(numsofnames[i]):
      job["args"].append(consumeoperationargs(job["name"],duprp))
     #
     joblist.append(job)

    #print (dictforjs)
    # Depending on methods, do what you wanna do:
    currenttime=time.strftime("%Y%m%d-%H%M%S",time.localtime())
    if ('createjson' in rp):
     tmp=json.dumps(dictforjs, sort_keys=True, indent=4)
     response=HttpResponse(tmp, content_type="text/plain")
     response['Content-Disposition'] = 'attachment; filename=%s.json' % (currenttime)
     return response
    elif ('execjson' in rp):
     if (role == "opsuser"):
      tmp=json.dumps(dictforjs, sort_keys=True, indent=4)
      with open(jsondir+currenttime+".json", "w") as f:
       f.write(tmp)
      return redirect(index)
     else:
      return HttpResponse("You are not authorized.")
    elif ('save' in rp):
     request.session['dictforjs']=dictforjs
     return redirect(index)
    else:
     return HttpResponse("ViewError: NoSuchActionDefined")


@csrf_exempt
def postjson(request):
    # web service json upload
    # for this view, I can't use csrf middleware ..
    role=get_authorization(request)
    currenttime=time.strftime("%Y%m%d-%H%M%S",time.localtime())
    rp=request.POST
    loadjson=request.FILES["putjson"].read() # hmm..
    dictforjs=json.loads(loadjson)
    if (role == "opsuser"):
      tmp=json.dumps(dictforjs, sort_keys=True, indent=4)
      with open(jsondir+currenttime+".json", "w") as f:
       f.write(tmp)
      return HttpResponse(tmp)

