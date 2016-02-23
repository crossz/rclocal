#!/bin/sh
. /etc/profile
exec $ROCKETMQ_HOME/bin/mqnamesrv >> /opt/logs/rmq.out 2>&1 
