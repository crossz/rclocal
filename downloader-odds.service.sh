#!/bin/sh
. /etc/profile

cd /opt/caiex-crawler
#java -cp caiex-crawler-downloader-0.0.1-SNAPSHOT.jar:downloader/lib/* com.caiex.download.DownloaderStart soccer odds --server.port=8889 --sporttery.match.period=600 --company.odds.period=60 --redis.sentinels=sentinel26479:26479 > /dev/null 2>&1
exec java -cp caiex-crawler-downloader-0.0.1-SNAPSHOT.jar:downloader/lib/* com.caiex.download.DownloaderStart soccer odds $CRAWLER_OPTS --server.port=8889 --sporttery.match.period=600 --company.odds.period=60 > /dev/null 2>&1
