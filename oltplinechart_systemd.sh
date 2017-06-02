#!/bin/sh
. /etc/profile

exec java -jar /opt/OLTPLINECHART/query-odds-linechart-1.0-SNAPSHOT.jar >> /opt/logs/linechart.out 2>&1
