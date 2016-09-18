#!/bin/sh
. /etc/profile

exec java -jar /opt/spider/spider-robot.jar clean >> /dev/null 2>&1

