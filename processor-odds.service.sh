#!/bin/sh
. /etc/profile

cd /opt/caiex-crawler/processor
nohup java -cp caiex-crawler-processor-0.0.1-SNAPSHOT.jar:lib/* com.caiex.process.ProcessorStart odds --nowgoal.company=31,3 --company.odds.period=30 > /dev/null 2>&1 &
