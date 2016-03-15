#!/bin/sh
. /etc/profile.d/caiex.sh
. /opt/spider/profile.d/caiex_matlab.sh
exec java -jar /opt/spider/spider-web.war >> /opt/logs/spider-web.out 2>&1
