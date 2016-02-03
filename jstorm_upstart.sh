#!/bin/sh
. /etc/profile
exec jstorm jar /opt/jstorm/rm.jar com.caiex.storm.StormStart >> /opt/logs/jstorm.out 2>&1 

