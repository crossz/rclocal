#!/bin/sh
. /etc/profile.d/caiex.sh
. /opt/spider/profile.d/caiex_matlab.sh
#exec java -jar /opt/spider/spider-web.war >> /opt/logs/spider-web.out 2>&1
exec java -jar /opt/spider/spider-web.war --rocket.mq.addr=10.46.176.181:9876 --endpoint.sbc.match_compare=https://10.45.8.228:12315/SBC/matchCompare.do --server.port=12316 >> /opt/logs/spider-web.out 2>&1
