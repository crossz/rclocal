#!/bin/sh
. /etc/profile
nohup java -jar /opt/dubbo/oltp-service-dubbo-1.0-SNAPSHOT.jar > /opt/logs/dubbo_nohup.out &

