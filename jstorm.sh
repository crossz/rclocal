#!/bin/sh
. /etc/profile
nohup jstorm jar /opt/jstorm/rm.jar com.caiex.storm.StormStart > /opt/logs/jstorm_nohup.out &

