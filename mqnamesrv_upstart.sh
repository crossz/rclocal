#!/bin/sh -ex
. /etc/profile

### global variables
#NAMESRV_ADDR='10.174.11.72:9876'
NAMESRV_ADDR=${HOST_IP}':9876'
export NAMESRV_ADDR


exec $ROCKETMQ_HOME/bin/mqnamesrv >> /opt/logs/rmq.out 2>&1 
