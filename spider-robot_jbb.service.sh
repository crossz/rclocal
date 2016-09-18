#!/bin/sh
. /etc/profile
#exec java -jar /opt/spider/spider-robot.jar jbb lj win310 pinnacle sportteryAll sporttery >> /opt/logs/spider-robot_all_temp.out 2>&1
#exec java -javaagent:/opt/spider/OneAPM/oneapm.jar -jar /opt/spider/spider-robot.jar jbb >> /dev/null 2>&1

exec java -jar /opt/spider/spider-robot.jar jbb >> /dev/null 2>&1
#exec java -jar /opt/spider/spider-robot.jar jbb >> /opt/logs/spider-robot_temp-jbb.out 2>&1

