#!/bin/sh
. /etc/profile.d/caiex.sh
exec $ROCKETMQ_HOME/bin/mqbroker -n 127.0.0.1:9876  >> /opt/logs/rmq.out 2>&1 
