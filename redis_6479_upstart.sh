#!/bin/sh -ex
. /etc/profile.d/caiex.sh
#exec $REDIS_HOME/26479/redis-sentinel $REDIS_HOME/26479/sentinel.conf >> /opt/logs/redis.out 2>&1 
exec $REDIS_HOME/6479/redis-server $REDIS_HOME/6479/redis.conf >> /opt/logs/redis.out 2>&1 
#exec $REDIS_HOME/6579/redis-server $REDIS_HOME/6579/redis.conf >> /opt/logs/redis.out 2>&1 
