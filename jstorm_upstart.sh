#!/bin/sh
. /etc/profile.d/caiex.sh
exec /opt/jstorm-2.1.1/bin/jstorm jar /opt/jstorm/rm-0.0.1-SNAPSHOT.jar com.caiex.storm.TestStormStart >> /opt/logs/jstorm.out 2>&1 
#exec jstorm jar /opt/jstorm/rm.jar com.caiex.storm.TestStormStart test >> /opt/logs/jstorm.out 2>&1 
#exec jstorm jar /opt/jstorm/rm-0.0.1-SNAPSHOT.jar com.caiex.storm.TestStormStart test

