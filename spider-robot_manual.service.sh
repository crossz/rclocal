#!/bin/sh
. /etc/profile

exec java -jar /opt/spider/spider-robot.jar manual >> /dev/null 2>&1

