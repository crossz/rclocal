#!/bin/sh
. /etc/profile.d/caiex.sh
. /opt/spider/profile.d/caiex_matlab.sh
exec java -jar /opt/spider/matlab-service.jar > /opt/logs/matlab_service.out 2>&1 
