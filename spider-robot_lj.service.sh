#!/bin/sh
. /etc/profile
#exec java -jar /opt/spider/spider-robot.jar jbb lj win310 pinnacle sportteryAll sporttery >> /opt/logs/spider-robot_all_temp.out 2>&1
exec java -jar /opt/spider/spider-robot.jar lj >> /dev/null 2>&1
