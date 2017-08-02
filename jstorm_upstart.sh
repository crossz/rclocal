#!/bin/sh
. /etc/profile
cd /opt/jstorm

jstorm jar rm-0.0.1-SNAPSHOT.jar com.caiex.storm.TestStormStart >> /opt/logs/jstorm.out 2>&1
