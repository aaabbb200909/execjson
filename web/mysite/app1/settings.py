
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
  'args': [_("server"), _("path"), _("owner"), _("group"), _("mode")]
 },
 {'jobname': _('filetransfer'),
  'args': [_("srcserver"), _("srcpath"), _("dstserver"), _("dstpath"), _("owner"), _("group"), _("mode")]
 },
 {'jobname': "deletefile",
  "args": [_("server"), _( "filepath")]
 },
 {'jobname': _("execshell"),
  "args": [_("server"), _("path"), _("user"), _("background")],
  "selectargs": {"background": [["yes", "yes"], ["no", "no"]]}
 },
 {'jobname': _("editcron"),
  "args": [_("operation"), _( "server"), _( "user"), _( "minute"), _( "hour"), _( "day"), _( "month"), _( "dayofweek"), _( "command")],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': _("editat"),
  "args": [_("operation"), _("server"), _("user"), _("minute"), _("hour"), _("day"), _("month"), _("year"), _("command")],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': _("mountnfs"),
  "args": [_("operation"), _("servername"), _("mountpoint"), _("mountoption"), _("nfsserver"), _("exportpath")],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': _("execsql"),
  "args": [_("operation"), _("dbname"), _("filename")]
 },
 {'jobname': "modifyuseros",
  "args": [_("operation"), _("server"), _("username"), _("firstname"), _("lastname"), _("groups")],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': _("passwdresetos"),
  "args": [_("server"), _("username")]
 },
 {'jobname': _("modifydns"),
  "args": [_("operation"), _("fqdn"), _("ipaddr")],
  "selectargs": {"operation": [["add", "add"], ["del", "del"]]}
 },
 {'jobname': _("addfirewallpolicy"),
  "args": [_("srcaddress"), _("srcnetmask"), _("destaddress"), _("destnetmask"), _("applicationname"), _("policy_then")]
 }
]

operationswithseveralops=['mkdir','filetransfer','editcron','editat', 
 'modifyuseros', 'passwdresetos', 'deletefile', "modifydns"
]
