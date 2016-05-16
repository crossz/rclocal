#!/bin/sh
. /etc/profile
exec java -jar /opt/spider/spider-robot.jar lj >> /dev/null 2>&1
#exec java -jar /opt/spider/spider-robot.jar lj >> /opt/logs/robot_lj.temp.log 2>&1 #/dev/null 2>&1
