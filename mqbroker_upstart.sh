#!/bin/sh
. /etc/profile

## global variables
NAMESRV_ADDR='10.171.127.205:9876'

exec $ROCKETMQ_HOME/bin/mqbroker -n $NAMESRV_ADDR >> /opt/logs/rmq.out 2>&1 
