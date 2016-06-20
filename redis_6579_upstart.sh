#!/bin/sh -ex
. /etc/profile
cd $REDIS_HOME
exec $REDIS_HOME/6579/redis-server $REDIS_HOME/6579/redis.conf >> /opt/logs/redis.out 2>&1 
