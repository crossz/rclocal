#!/bin/sh
. /etc/profile
exec $CATALINA_HOME/bin/catalina.sh run >> /opt/logs/catalina.out 2>&1
