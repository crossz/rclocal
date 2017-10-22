#!/bin/sh
. /etc/profile

cd /opt/caiex-crawler
exec java -cp caiex-crawler-processor-0.0.1-SNAPSHOT.jar:processor/lib/* com.caiex.process.ProcessorStart soccer odds $CRAWLER_OPTS --nowgoal.company=24,3 --company.odds.period=30 > /dev/null 2>&1
