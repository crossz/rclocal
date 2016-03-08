#!/bin/sh
. /etc/profile.d/caiex.sh
exec java -jar /opt/spider/spider-robot.jar jbb lj jbb3 lj3 win310 pinnacle sportteryAll sporttery >> /opt/logs/spider-robot.out 2>&1
