#!/bin/sh
. /etc/profile.d/caiex.sh
exec $CATALINA_HOME/bin/catalina.sh run >> /opt/logs/catalina.out 2>&1
