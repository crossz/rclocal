#!/bin/sh
. /etc/profile.d/caiex.sh
. /opt/spider/profile.d/caiex_matlab.sh
exec java -jar /opt/spider/spider-web.war --rocket.mq.addr=10.174.11.76:9876 --endpoint.sbc.match_compare=https://10.174.11.76:12315/SBC/matchCompare.do --server.port=12316 >> /opt/logs/spider-web.out 2>&1
