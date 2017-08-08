#!/bin/sh
. /etc/profile

cd /opt/caiex-crawler/downloader
nohup java -cp caiex-crawler-downloader-0.0.1-SNAPSHOT.jar:lib/* com.caiex.download.DownloaderStart score > /dev/null 2>&1 &
