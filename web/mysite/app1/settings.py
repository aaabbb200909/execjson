
##
# application specific defs
##
import mysite.settings
from django.utils.translation import ugettext_noop as _


jsondir=mysite.settings.BASE_DIR+'/../../tmp/jsondir/'
logdir="/var/www/html/execjson/"
use_authorization=False # let this be True, if you want to use authorization feature
role_opsusers=['user1']
role_applusers=['user2']
use_workflow=False # let this be True, if you want to use workflow feature
role_managers=['user9']
use_svg_form=False # If True, template will be use svg feature in its HTML form
jobs=[
 {'jobname': _('mkdir'),
  'args': [_("server"), "path", "owner", "group", "mode"]
 },
 {'jobname': 'filetransfer',
  'args': ["srcserver", "srcpath", "dstserver", "dstpath", "owner", "group", "mode"]
 },
 {'jobname': "deletefile",
  "args": ["server", "filepath"]
 },
 {'jobname': "execshell",
  "args": ["server", "path", "user", "background"],
  "selectargs": {"background": [["yes", "yes"], ["no", "no"]]}
 },
 {'jobname': "editcron",
  "args": ["operation", "server", "user", "minute", "hour", "day", "month", "dayofweek", "command"],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': "editat",
  "args": ["operation", "server", "user", "minute", "hour", "day", "month", "year", "command"],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': "mountnfs",
  "args": ["operation", "servername", "mountpoint", "mountoption", "nfsserver", "exportpath"],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': "execsql",
  "args": ["operation", "dbname", "filename"]
 },
 {'jobname': "modifyuseros",
  "args": ["operation", "server", "username", "firstname", "lastname" ,"groups"],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': "passwdresetos",
  "args": ["server", "username"]
 },
 {'jobname': "modifydns",
  "args": ["operation", "fqdn", "ipaddr"],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': "addfirewallpolicy",
  "args": ["srcaddress", "srcnetmask", "destaddress", "destnetmask", "applicationname", "policy_then"]
 }
]


operationswithseveralops=['mkdir','filetransfer','editcron','editat', 
 'modifyuseros', 'passwdresetos', 'deletefile', "modifydns"
]
