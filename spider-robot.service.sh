#!/bin/sh
. /etc/profile.d/caiex.sh
#exec java -javaagent:/opt/spider/OneAPM/oneapm.jar -jar /opt/spider/spider-robot.jar win310 pinnacle sportteryAll sporttery >> /dev/null 2>&1
#exec java -jar /opt/spider/spider-robot.jar jbb lj win310 pinnacle sportteryAll sporttery >> /opt/logs/spider-robot_all_temp.out 2>&1
#exec java -jar /opt/spider/spider-robot.jar win310 pinnacle sportteryAll sporttery >> /dev/null 2>&1
exec java -jar /opt/spider/spider-robot.jar win310 sportteryAll sporttery statistic >> /dev/null 2>&1 #remove pinnacle temporarly
