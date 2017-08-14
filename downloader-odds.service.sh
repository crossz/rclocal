#!/bin/sh
. /etc/profile

cd /opt/caiex-crawler/downloader
nohup java -cp caiex-crawler-downloader-0.0.1-SNAPSHOT.jar:lib/* com.caiex.download.DownloaderStart odds --server.port=8889 --sporttery.match.period=600 --company.odds.period=60 > /dev/null 2>&1 &
