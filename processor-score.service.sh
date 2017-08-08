#!/bin/sh
. /etc/profile

cd /opt/caiex-crawler/processor
nohup java -cp caiex-crawler-processor-0.0.1-SNAPSHOT.jar:lib/* com.caiex.process.ProcessorStart score > /dev/null 2>&1 &
