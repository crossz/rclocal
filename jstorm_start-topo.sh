#!/bin/sh
. /etc/profile

cd /opt/jstorm
jstorm jar rm-0.0.1-SNAPSHOT.jar com.caiex.storm.TestStormStart trade >> /opt/logs/jstorm.out

echo 'please wait for 30s'
sleep 30
