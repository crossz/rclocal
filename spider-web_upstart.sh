#!/bin/sh
. /etc/profile.d/caiex.sh
exec java -jar /opt/spider/spider-web.war >> /opt/logs/spider-web.out 2>&1
