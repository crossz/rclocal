#!/bin/sh
. /etc/profile

### global variables
##: need configure in /etc/profile.d/caiex.sh
#NAMESRV_ADDR='10.171.127.205:9876'

exec $ROCKETMQ_HOME/bin/mqnamesrv >> /opt/logs/rmq.out 2>&1 
