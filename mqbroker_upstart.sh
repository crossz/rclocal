#!/bin/sh
. /etc/profile

### global variables
NAMESRV_ADDR='127.0.0.1:9876'
export NAMESRV_ADDR

exec $ROCKETMQ_HOME/bin/mqbroker -n $NAMESRV_ADDR >> /opt/logs/rmq.out 2>&1 
