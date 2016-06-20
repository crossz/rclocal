#!/bin/sh -ex
. /etc/profile
cd $REDIS_HOME
exec $REDIS_HOME/26479/redis-sentinel $REDIS_HOME/26479/sentinel.conf >> /opt/logs/redis.out 2>&1 
