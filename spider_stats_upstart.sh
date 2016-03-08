#!/bin/sh
. /etc/profile.d/caiex.sh
exec java -jar /opt/spider/spider-robot.jar statistic >> /opt/logs/spider-robot.out 2>&1
