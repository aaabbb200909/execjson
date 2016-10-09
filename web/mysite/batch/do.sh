jsondir="/var/tmp/execjson/tmp/jsondir/"
bindir=$(dirname $0)
logdir="/var/www/html/execjson/"

cd ${bindir} # fabfile is there
while true
do
 date
 for jsonfile in $jsondir/*json
 do
  jsonname=$(basename ${jsonfile})
  if [[ ! -f ${jsonfile}.state  ]]
  then
   echo "exec:" ${jsonfile}
   applcode=$(grep jobapplcode ${jsonfile} | awk -F: '{print $2}' | awk -F\" '{print $2}' )
   if [[ -n ${applcode} ]]
   then
    logdir=${logdir}/${applcode}
   fi
   echo logdir: $logdir
   ${bindir}/do.py ${jsonfile} > ${logdir}/${jsonname}.txt 2>&1 &
  fi
 done
 echo ""
 sleep 15
done
