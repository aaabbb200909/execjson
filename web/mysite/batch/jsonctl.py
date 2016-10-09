#!/usr/bin/env python
import json, sys
argc=len(sys.argv)
if (not (argc in [2,3,4])):
 print "usage: %s [dumpall/dump/get/set] [number] [notyet/ongoing/done]" % sys.argv[0]
 sys.exit(31)
command=sys.argv[1]
if (argc>2):
 number=sys.argv[2]
 if (argc>3):
  state=sys.argv[3]
  if(not state in ["notyet", "ongoing", "done"]):
   raise Exception
 
def dumpall(js):
 print json.dumps(js, indent=4)

js=json.loads(sys.stdin.read())
if (command=="dumpall"):
 dumpall(js)
elif (command=="dump"):
 tmp=[j["state"] for j in js]
 for i in range(len(tmp)):
  print i, ':',tmp[i]
elif (command=="get"):
 print js[int(number)]["state"]
elif (command=="set"):
 js[int(number)]["state"]=state
 dumpall(js)
else:
 raise Exception
