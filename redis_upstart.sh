#!/bin/sh
. /etc/profile.d/caiex.sh
exec $REDIS_HOME/src/redis-server $REDIS_HOME/redis.conf >> /opt/logs/redis.out 2>&1 
