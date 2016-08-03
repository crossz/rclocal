#!/bin/sh
. /etc/profile

### global variables
##: need configure in /etc/profile.d/caiex.sh
#NAMESRV_ADDR='192.168.1.4:9876'

exec $ROCKETMQ_HOME/bin/mqbroker -n $NAMESRV_ADDR -c /opt/alibaba-rocketmq/conf/2m-noslave/broker-a.properties  >> /opt/logs/rmq.out 2>&1 
