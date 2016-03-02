#!/bin/sh
. /etc/profile.d/caiex.sh
exec $ZOOKEEPER_HOME/bin/zkServer.sh start-foreground >> /opt/logs/zookeeper.out 2>&1 
