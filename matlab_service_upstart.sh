#!/bin/sh
. /etc/profile
exec java -jar /opt/spider/matlab-service.jar > /opt/logs/matlab_service.out 2>&1 

