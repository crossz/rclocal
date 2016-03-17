#!/bin/sh
. /etc/profile.d/caiex.sh
. /opt/spider/profile.d/caiex_matlab.sh
exec java -jar /opt/spider/spider-web.war --Drocket.mq.addr=192.168.1.154:9876 --Dendpoint.sbc.match_compare=http://192.168.1.6:8080/SBC/matchCompare.do --Dserver.port=8086 >> /opt/logs/spider-web.out 2>&1
