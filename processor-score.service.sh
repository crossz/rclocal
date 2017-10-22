#!/bin/sh
. /etc/profile

cd /opt/caiex-crawler
exec java -cp caiex-crawler-processor-0.0.1-SNAPSHOT.jar:processor/lib/* com.caiex.process.ProcessorStart soccer score $CRAWLER_OPTS --score.period=15 > /dev/null 2>&1
