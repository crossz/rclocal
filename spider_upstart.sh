#!/bin/sh
. /etc/profile
exec java -jar /opt/spider/spider-robot.jar >> /opt/logs/spider-robot.out 2>&1
