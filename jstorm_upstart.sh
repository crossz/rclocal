#!/bin/sh
. /etc/profile.d/caiex.sh
exec jstorm jar /opt/jstorm/rm.jar com.caiex.storm.StormStart >> /opt/logs/jstorm.out 2>&1 

