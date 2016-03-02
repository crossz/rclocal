#!/bin/sh
. /etc/profile.d/caiex.sh
exec $ROCKETMQ_HOME/bin/mqnamesrv >> /opt/logs/rmq.out 2>&1 
