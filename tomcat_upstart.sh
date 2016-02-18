#!/bin/sh
. /etc/profile
exec $CATALINA_HOME/bin/catalina.sh run >> /opt/logs/$job.log 2>&1 >> /opt/logs/catalina.out 2>&1
