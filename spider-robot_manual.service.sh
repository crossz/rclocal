#!/bin/sh
. /etc/profile

exec java -jar /opt/spider/spider-robot.jar manual >> /opt/logs/manual.log 2>&1

