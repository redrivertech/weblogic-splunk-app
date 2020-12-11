#!/bin/bash

#. /opt/weblogic/wlserver_10.3/server/bin/setWLSEnv.sh
#export BEA_HOME=/opt/weblogic
#export SPLUNK_HOME=/opt/splunkforwarder/

. $1/bin/setWlstEnv.sh


for((i=1;i<=$DOMAIN_COUNT;i++))
do(
        eval TMP_DOMAIN_PATH=\${DOMAIN_PATH_${i}}
        if [ -d $TMP_DOMAIN_PATH ]
        then
                cd $TMP_DOMAIN_PATH
                java  -classpath $2/wlserver_10.3/server/lib/weblogic.jar weblogic.WLST $1/bin/wlsCollectJmxDataDaily.py $i
        fi
)
done
