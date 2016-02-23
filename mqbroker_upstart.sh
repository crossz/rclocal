#!/bin/sh
. /etc/profile
exec $ROCKETMQ_HOME/bin/mqbroker -n $NAMESRV_ADDR >> /opt/logs/rmq.out 2>&1 
