#!/bin/sh -ex
. /etc/profile
cd $REDIS_HOME/26579
exec $REDIS_HOME/26579/redis-sentinel $REDIS_HOME/26579/sentinel.conf >> /opt/logs/redis.out 2>&1 
