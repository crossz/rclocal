#!/bin/sh
. /etc/profile

cd /opt/caiex-crawler
exec java -cp caiex-crawler-downloader-0.0.1-SNAPSHOT.jar:downloader/lib/* com.caiex.download.DownloaderStart soccer score $CRAWLER_OPTS --score.period=10 > /dev/null 2>&1
