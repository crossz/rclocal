#!/bin/sh
. /etc/profile.d/caiex.sh
nohup java -jar /opt/consumer/oltp-service-consumer-1.0-SNAPSHOT.jar > /opt/logs/consumer_nohup.out &
