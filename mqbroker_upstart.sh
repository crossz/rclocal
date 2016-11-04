#!/bin/sh
. /etc/profile

### global variables
NAMESRV_ADDR='10.174.11.72:9876'
export NAMESRV_ADDR

echo 'name server is: '$NAMESRV_ADDR >> /opt/logs/rmq.out
<<<<<<< HEAD
exec $ROCKETMQ_HOME/bin/mqbroker -n $NAMESRV_ADDR -c /opt/alibaba-rocketmq/conf/2m-noslave/broker-a.properties >> /opt/logs/rmq.out 2>&1 
=======
exec $ROCKETMQ_HOME/bin/mqbroker -n $NAMESRV_ADDR -c /opt/alibaba-rocketmq/conf/2m-noslave/broker-a.properties >> /opt/logs/rm
q.out 2>&1
>>>>>>> 43a1275c6e8d13342721a8845d346f1f765ca308
