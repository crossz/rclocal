#!/bin/sh
. /etc/profile.d/caiex.sh
#[ -e /opt/sbcconsumer ] && . /opt/sbcconsumer/profile.d/caiex_matlab.sh
exec $CATALINA_HOME/bin/catalina.sh run >> /opt/logs/catalina.out 2>&1
