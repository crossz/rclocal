#!/bin/sh
. /etc/profile
#exec java -javaagent:/opt/spider/OneAPM/oneapm.jar -jar /opt/spider/spider-robot.jar 500 >> /dev/null 2>&1

#exec java -javaagent:/opt/spider/OneAPM/oneapm.jar -jar /opt/spider/spider-robot.jar 500 >> /opt/logs/spider-robot_500_temp.out 2>&1
#exec java -jar /opt/spider/spider-robot.jar 500 >> /opt/logs/spider-robot_500_temp.out # >> /dev/null 2>&1
exec java -jar /opt/spider/spider-robot.jar 500 >> /dev/null 2>&1
