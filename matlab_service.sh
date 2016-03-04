#!/bin/sh
. /etc/profile.d/caiex.sh
nohup java -jar /opt/spider/matlab-service.jar > /opt/logs/matlab_service_nohup.out 2>&1 &

