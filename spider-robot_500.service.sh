#!/bin/sh
. /etc/profile.d/caiex.sh
exec java -jar /opt/spider/spider-robot.jar 500 >> /dev/null 2>&1
