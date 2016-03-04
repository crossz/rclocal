#!/bin/sh
. /etc/profile.d/caiex.sh
nohup jstorm jar /opt/jstorm/rm.jar com.caiex.storm.StormStart > /opt/logs/jstorm_nohup.out &

