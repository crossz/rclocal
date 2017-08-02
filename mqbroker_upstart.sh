#!/bin/sh -ex
. /etc/profile

### global variables
#NAMESRV_ADDR='10.174.11.72:9876'
NAMESRV_ADDR=${HOST_IP}':9876'
export NAMESRV_ADDR

echo 'name server is: '$NAMESRV_ADDR >> /opt/logs/rmq.out
exec $ROCKETMQ_HOME/bin/mqbroker -n $NAMESRV_ADDR -c /opt/alibaba-rocketmq/conf/2m-noslave/broker-a.properties >> /opt/logs/rmq.out 2>&1 
