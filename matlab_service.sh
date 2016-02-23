#!/bin/sh
. /etc/profile
nohup java -jar /opt/spider/matlab-service.jar > /opt/logs/matlab_service_nohup.out 2>&1 &

